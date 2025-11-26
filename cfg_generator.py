"""
CFG Generator: Transform WhileD AST to Control Flow Graph

This module implements the core transformation logic:
1. Expression flattening (linearization)
2. Short-circuit evaluation handling
3. Statement processing (control flow generation)
4. Basic block construction from linear IR
"""

from typing import List, Tuple, Dict
from ast_definition import *
from ir_representation import *


class CFGGenerator:
    """Generates Control Flow Graph from WhileD AST."""
    
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
    
    # ==================
    # Helper Functions
    # ==================
    
    def fresh_temp(self) -> str:
        """Generate a new unique temporary variable.
        
        Returns: "#0", "#1", "#2", etc.
        """
        temp = f"#{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def fresh_label(self) -> str:
        """Generate a new unique label.
        
        Returns: "LABEL_1", "LABEL_2", etc.
        """
        self.label_counter += 1
        return f"LABEL_{self.label_counter}"
    
    # ==================
    # Expression Flattener
    # ==================
    
    def flatten_expr(self, expr: Expr) -> Tuple[List[Instruction], str]:
        """Flatten an expression into linear IR instructions.
        
        Args:
            expr: The expression to flatten
            
        Returns:
            (instructions, result_variable): The list of IR instructions
            and the variable holding the final result
        """
        
        if isinstance(expr, EConst):
            # Constants can be used directly as operands
            return ([], str(expr.value))
        
        elif isinstance(expr, EVar):
            # Variables can be used directly
            return ([], expr.name)
        
        elif isinstance(expr, EBinop):
            # Handle short-circuit operators specially
            if expr.op in ['&&', '||']:
                return self.flatten_shortcircuit(expr.op, expr.left, expr.right)
            
            # Regular binary operation
            left_instrs, left_var = self.flatten_expr(expr.left)
            right_instrs, right_var = self.flatten_expr(expr.right)
            
            result_temp = self.fresh_temp()
            result_instr = IRBinOp(result_temp, left_var, expr.op, right_var)
            
            return (left_instrs + right_instrs + [result_instr], result_temp)
        
        elif isinstance(expr, EUnop):
            # Unary operation
            operand_instrs, operand_var = self.flatten_expr(expr.expr)
            
            result_temp = self.fresh_temp()
            unop_instr = IRUnOp(result_temp, expr.op, operand_var)
            
            return (operand_instrs + [unop_instr], result_temp)
        
        elif isinstance(expr, EDeref):
            # Dereference: *e
            addr_instrs, addr_var = self.flatten_expr(expr.expr)
            
            result_temp = self.fresh_temp()
            deref_instr = IRDeref(result_temp, addr_var)
            
            return (addr_instrs + [deref_instr], result_temp)
        
        elif isinstance(expr, EAddrOf):
            # Address-of: &e
            # Note: e should be an L-value (typically EVar)
            if isinstance(expr.expr, EVar):
                result_temp = self.fresh_temp()
                addrof_instr = IRAddrOf(result_temp, expr.expr.name)
                return ([addrof_instr], result_temp)
            else:
                # For more complex expressions, flatten first
                # (though semantically this might be invalid)
                inner_instrs, inner_var = self.flatten_expr(expr.expr)
                result_temp = self.fresh_temp()
                addrof_instr2 = IRAddrOf(result_temp, inner_var)
                return (inner_instrs + [addrof_instr2], result_temp)
        
        else:
            raise ValueError(f"Unknown expression type: {type(expr)}")
    
    # ==================
    # Short-Circuit Handler
    # ==================
    
    def flatten_shortcircuit(self, op: str, left: Expr, right: Expr) -> Tuple[List[Instruction], str]:
        """Handle short-circuit evaluation for && and ||.
        
        Converts logical operators into control flow with jumps.
        
        For e1 && e2:
            Evaluate e1 -> #t
            if (!#t) then jmp FALSE_LABEL
            Evaluate e2 -> #t (reuse same temp)
            jmp END_LABEL
            FALSE_LABEL:
            #t = 0
            END_LABEL:
        
        For e1 || e2:
            Evaluate e1 -> #t
            if (#t) then jmp TRUE_LABEL  (need to invert)
            Evaluate e2 -> #t
            jmp END_LABEL
            TRUE_LABEL:
            #t = 1
            END_LABEL:
        """
        
        result_temp = self.fresh_temp()
        instructions = []
        
        if op == '&&':
            # AND: Short-circuit if left is false
            false_label = self.fresh_label()
            end_label = self.fresh_label()
            
            # Evaluate left
            left_instrs, left_var = self.flatten_expr(left)
            instructions.extend(left_instrs)
            instructions.append(IRAssign(result_temp, left_var))
            
            # If left is false, jump to false_label
            instructions.append(IRCondJump(result_temp, false_label))
            
            # Evaluate right (only if left was true)
            right_instrs, right_var = self.flatten_expr(right)
            instructions.extend(right_instrs)
            instructions.append(IRAssign(result_temp, right_var))
            
            # Jump to end
            instructions.append(IRJump(end_label))
            
            # False label: set result to 0
            instructions.append(IRLabel(false_label))
            instructions.append(IRAssign(result_temp, "0"))
            
            # End label
            instructions.append(IRLabel(end_label))
        
        elif op == '||':
            # OR: Short-circuit if left is true
            # We need to check if left is true, but we only have "if (! cond)"
            # So we invert the logic: if left is false, evaluate right
            
            true_label = self.fresh_label()
            end_label = self.fresh_label()
            
            # Evaluate left
            left_instrs, left_var = self.flatten_expr(left)
            instructions.extend(left_instrs)
            instructions.append(IRAssign(result_temp, left_var))
            
            # If left is false (!left is true), skip to evaluating right
            instructions.append(IRCondJump(result_temp, self.fresh_label()))  # temp label for "not true" path
            
            # Left is true: set result to 1 and jump to end
            instructions.append(IRAssign(result_temp, "1"))
            instructions.append(IRJump(end_label))
            
            # Left is false: evaluate right
            # Re-insert the label we created above
            instructions[-3] = IRCondJump(result_temp, self.label_counter)  # Fix this
            
            # Let me rewrite this more clearly:
            instructions = []
            false_label = self.fresh_label()
            end_label = self.fresh_label()
            
            # Evaluate left
            left_instrs, left_var = self.flatten_expr(left)
            instructions.extend(left_instrs)
            instructions.append(IRAssign(result_temp, left_var))
            
            # If left is false, evaluate right
            instructions.append(IRCondJump(result_temp, false_label))
            
            # Left is true: result is already set to left_var (true/1)
            # Just jump to end
            instructions.append(IRJump(end_label))
            
            # False label: evaluate right
            instructions.append(IRLabel(false_label))
            right_instrs, right_var = self.flatten_expr(right)
            instructions.extend(right_instrs)
            instructions.append(IRAssign(result_temp, right_var))
            
            # End label
            instructions.append(IRLabel(end_label))
        
        return (instructions, result_temp)
    
    # ==================
    # Statement Processor (Phase 1: AST → Linear IR)
    # ==================
    
    def process_statement(self, stmt: Com) -> List[Instruction]:
        """Process a statement and generate linear IR instructions.
        
        Args:
            stmt: The statement to process
            
        Returns:
            List of IR instructions (linear, with labels and jumps)
        """
        
        if isinstance(stmt, CSkip):
            # Empty statement
            return []
        
        elif isinstance(stmt, CAsgnVar):
            # Variable assignment: x = e
            expr_instrs, expr_var = self.flatten_expr(stmt.expr)
            
            # Final assignment
            assign_instr = IRAssign(stmt.var, expr_var)
            
            return expr_instrs + [assign_instr]
        
        elif isinstance(stmt, CAsgnDeref):
            # Pointer assignment: *e1 = e2
            addr_instrs, addr_var = self.flatten_expr(stmt.addr)
            value_instrs, value_var = self.flatten_expr(stmt.value)
            
            store_instr = IRStoreDeref(addr_var, value_var)
            
            return addr_instrs + value_instrs + [store_instr]
        
        elif isinstance(stmt, CSeq):
            # Sequential composition: c1; c2
            first_instrs = self.process_statement(stmt.first)
            second_instrs = self.process_statement(stmt.second)
            
            return first_instrs + second_instrs
        
        elif isinstance(stmt, CIf):
            # If-else statement
            # Pattern:
            #   [cond_instrs]
            #   if (!cond) then jmp ELSE_LABEL
            #   [then_instrs]
            #   jmp END_LABEL
            # ELSE_LABEL:
            #   [else_instrs]
            # END_LABEL:
            
            else_label = self.fresh_label()
            end_label = self.fresh_label()
            
            instructions = []
            
            # Condition evaluation
            cond_instrs, cond_var = self.flatten_expr(stmt.cond)
            instructions.extend(cond_instrs)
            
            # If condition is false, jump to else
            instructions.append(IRCondJump(cond_var, else_label))
            
            # Then branch
            then_instrs = self.process_statement(stmt.then_branch)
            instructions.extend(then_instrs)
            
            # Jump to end (skip else)
            instructions.append(IRJump(end_label))
            
            # Else label and branch
            instructions.append(IRLabel(else_label))
            else_instrs = self.process_statement(stmt.else_branch)
            instructions.extend(else_instrs)
            
            # End label
            instructions.append(IRLabel(end_label))
            
            return instructions
        
        elif isinstance(stmt, CWhile):
            # While loop
            # Pattern:
            # START_LABEL:
            #   [cond_instrs]
            #   if (!cond) then jmp END_LABEL
            #   [body_instrs]
            #   jmp START_LABEL
            # END_LABEL:
            
            start_label = self.fresh_label()
            end_label = self.fresh_label()
            
            instructions = []
            
            # Start label
            instructions.append(IRLabel(start_label))
            
            # Condition evaluation
            cond_instrs, cond_var = self.flatten_expr(stmt.cond)
            instructions.extend(cond_instrs)
            
            # If condition is false, exit loop
            instructions.append(IRCondJump(cond_var, end_label))
            
            # Body
            body_instrs = self.process_statement(stmt.body)
            instructions.extend(body_instrs)
            
            # Jump back to start
            instructions.append(IRJump(start_label))
            
            # End label
            instructions.append(IRLabel(end_label))
            
            return instructions
        
        else:
            raise ValueError(f"Unknown statement type: {type(stmt)}")
    
    # ==================
    # CFG Construction (Phase 2: Linear IR → Basic Block Graph)
    # ==================
    
    def build_cfg(self, instructions: List[Instruction]) -> List[BasicBlock]:
        """Convert linear instruction list into a Control Flow Graph.
        
        Algorithm:
        1. Identify leaders (starts of basic blocks)
        2. Create BasicBlock objects
        3. Connect edges (successors/predecessors)
        
        Args:
            instructions: Linear list of IR instructions
            
        Returns:
            List of connected BasicBlock objects
        """
        
        if not instructions:
            return []
        
        # Step 1: Identify leaders
        leaders = self._identify_leaders(instructions)
        
        # Step 2: Create basic blocks
        blocks, label_to_block = self._create_blocks(instructions, leaders)
        
        # Step 3: Connect edges
        self._connect_edges(blocks, label_to_block)
        
        return blocks
    
    def _identify_leaders(self, instructions: List[Instruction]) -> set:
        """Identify leader instructions (starts of basic blocks).
        
        Leaders are:
        1. The first instruction
        2. Target of any jump
        3. Instruction immediately following a jump
        """
        leaders = set()
        
        # First instruction is always a leader
        if instructions:
            leaders.add(0)
        
        # Build label-to-index map
        label_to_idx = {}
        for i, instr in enumerate(instructions):
            if isinstance(instr, IRLabel):
                label_to_idx[instr.name] = i
        
        # Find jump targets and instructions after jumps
        for i, instr in enumerate(instructions):
            if isinstance(instr, (IRJump, IRCondJump)):
                # Target of jump is a leader
                target_label = instr.label
                if target_label in label_to_idx:
                    leaders.add(label_to_idx[target_label])
                
                # Instruction after jump is a leader
                if i + 1 < len(instructions):
                    leaders.add(i + 1)
        
        return leaders
    
    def _create_blocks(self, instructions: List[Instruction], leaders: set) -> Tuple[List[BasicBlock], Dict[str, BasicBlock]]:
        """Create BasicBlock objects from instructions.
        
        Returns:
            (blocks, label_to_block): List of blocks and mapping from labels to blocks
        """
        blocks = []
        label_to_block = {}
        
        # Sort leaders
        leader_list = sorted(leaders)
        
        # Create blocks
        for block_idx, leader_pos in enumerate(leader_list):
            block = BasicBlock(block_idx)
            
            # Determine end of this block
            if block_idx + 1 < len(leader_list):
                end_pos = leader_list[block_idx + 1]
            else:
                end_pos = len(instructions)
            
            # Process instructions in this block
            current_label = None
            for i in range(leader_pos, end_pos):
                instr = instructions[i]
                
                if isinstance(instr, IRLabel):
                    # Store label for this block
                    if current_label is None:
                        current_label = instr.name
                        block.label = instr.name
                        label_to_block[instr.name] = block
                
                elif isinstance(instr, (IRJump, IRCondJump)):
                    # This is a terminator
                    block.set_terminator(instr)
                
                else:
                    # Regular instruction
                    block.add_instruction(instr)
            
            blocks.append(block)
        
        return blocks, label_to_block
    
    def _connect_edges(self, blocks: List[BasicBlock], label_to_block: Dict[str, BasicBlock]):
        """Connect basic blocks based on control flow.
        
        Rules:
        - Unconditional jump: 1 successor (target)
        - Conditional jump: 2 successors (target + fall-through)
        - No jump (fall-through): 1 successor (next block)
        - Last block with no jump: 0 successors (exit)
        """
        for i, block in enumerate(blocks):
            if block.terminator is None:
                # No terminator: fall through to next block
                if i + 1 < len(blocks):
                    block.add_successor(blocks[i + 1])
            
            elif isinstance(block.terminator, IRJump):
                # Unconditional jump: 1 successor
                target_label = block.terminator.label
                if target_label in label_to_block:
                    block.add_successor(label_to_block[target_label])
            
            elif isinstance(block.terminator, IRCondJump):
                # Conditional jump: 2 successors
                # 1. Jump target (when condition is false, i.e., !cond is true)
                target_label = block.terminator.label
                if target_label in label_to_block:
                    block.add_successor(label_to_block[target_label])
                
                # 2. Fall-through (when condition is true, i.e., !cond is false)
                if i + 1 < len(blocks):
                    block.add_successor(blocks[i + 1])
    
    # ==================
    # Main Entry Point
    # ==================
    
    def _convert_labels_to_bb(self, instructions: List[Instruction]) -> List[Instruction]:
        """将 LABEL_ 标签转换为 BB_ 标签
        
        Args:
            instructions: 使用LABEL_标签的指令列表
            
        Returns:
            使用BB_标签的指令列表
        """
        # 建立 LABEL_ 到 BB_ 的映射
        label_map: dict[str, str] = {}
        bb_counter = 0
        
        # 第一遍：找到所有标签并建立映射
        for instr in instructions:
            if isinstance(instr, IRLabel):
                if instr.name not in label_map:
                    bb_counter += 1
                    label_map[instr.name] = f"BB_{bb_counter}"
        
        # 第二遍：转换所有指令
        converted: List[Instruction] = []
        for instr in instructions:
            if isinstance(instr, IRLabel):
                converted.append(IRLabel(label_map[instr.name]))
            elif isinstance(instr, IRJump):
                converted.append(IRJump(label_map.get(instr.label, instr.label)))
            elif isinstance(instr, IRCondJump):
                converted.append(IRCondJump(instr.cond, label_map.get(instr.label, instr.label)))
            else:
                converted.append(instr)
        
        return converted
    
    def generate_cfg(self, program: Com) -> ControlFlowGraph:
        """Complete pipeline: AST → CFG.
        
        Phase 1: Generate linear IR with LABEL_ (表达式拆分)
        Phase 2: Convert to BB_ format (基本块)
        Phase 3: Build CFG structure
        
        Args:
            program: WhileD program (AST)
            
        Returns:
            Control Flow Graph
        """
        # Phase 1: Generate linear IR with LABEL_
        instructions = self.process_statement(program)
        
        # 确保第一条指令前有入口标签
        if instructions and not isinstance(instructions[0], IRLabel):
            instructions.insert(0, IRLabel("LABEL_entry"))
        
        # Phase 2: Convert LABEL_ to BB_
        bb_instructions = self._convert_labels_to_bb(instructions)
        
        # Phase 3: Build CFG
        blocks = self.build_cfg(bb_instructions)
        
        # 返回 CFG，同时保存两个版本的IR
        cfg = ControlFlowGraph(blocks)
        cfg.linear_ir = instructions  # LABEL版本
        cfg.bb_ir = bb_instructions   # BB版本
        
        return cfg

