"""
Intermediate Representation (IR) and Control Flow Graph (CFG) Structure

This module defines:
1. IR instruction types (linearized, single-operation instructions)
2. BasicBlock class (nodes of the CFG)
3. ControlFlowGraph class (the complete CFG)
"""

from dataclasses import dataclass
from typing import List, Optional


# =======================
# IR Instruction Classes
# =======================

@dataclass
class IRAssign:
    """Simple assignment: dest = source
    
    Example: x = #0
    """
    dest: str
    source: str
    
    def __str__(self):
        return f"{self.dest} = {self.source}"

@dataclass
class IRBinOp:
    """Binary operation: dest = left op right
    
    Example: #0 = x + y
    """
    dest: str
    left: str
    op: str
    right: str
    
    def __str__(self):
        # Comparison and logical operators need parentheses
        comparison_ops = {'<', '<=', '>', '>=', '==', '!=', '&&', '||'}
        if self.op in comparison_ops:
            return f"{self.dest} = ({self.left} {self.op} {self.right})"
        else:
            return f"{self.dest} = {self.left} {self.op} {self.right}"

@dataclass
class IRUnOp:
    """Unary operation: dest = op operand
    
    Example: #0 = ! x
    """
    dest: str
    op: str
    operand: str
    
    def __str__(self):
        return f"{self.dest} = {self.op} {self.operand}"

@dataclass
class IRDeref:
    """Load from address: dest = *addr
    
    Example: #0 = *p
    """
    dest: str
    addr: str
    
    def __str__(self):
        return f"{self.dest} = *{self.addr}"

@dataclass
class IRAddrOf:
    """Get address of variable: dest = &var
    
    Example: #0 = &x
    """
    dest: str
    var: str
    
    def __str__(self):
        return f"{self.dest} = &{self.var}"

@dataclass
class IRStoreDeref:
    """Store to address: *addr = value
    
    Example: *#0 = #1
    """
    addr: str
    value: str
    
    def __str__(self):
        return f"*{self.addr} = {self.value}"

@dataclass
class IRLabel:
    """Label marker: LABEL_1:
    
    Marks a target for jumps.
    """
    name: str
    
    def __str__(self):
        return f"{self.name}:"

@dataclass
class IRCondJump:
    """Conditional jump: if (! cond) then jmp label
    
    Example: if (! #0) then jmp LABEL_2
    """
    cond: str
    label: str
    
    def __str__(self):
        return f"if (! {self.cond}) then jmp {self.label}"

@dataclass
class IRJump:
    """Unconditional jump: jmp label
    
    Example: jmp LABEL_1
    """
    label: str
    
    def __str__(self):
        return f"jmp {self.label}"


# Type alias for any IR instruction
Instruction = IRAssign | IRBinOp | IRUnOp | IRDeref | IRAddrOf | IRStoreDeref | IRLabel | IRCondJump | IRJump


# =======================
# Basic Block (CFG Node)
# =======================

class BasicBlock:
    """A basic block in the control flow graph.
    
    Properties:
    - id: Unique identifier
    - label: Optional label name if block starts with a label
    - instructions: List of IR instructions (no jumps stored here)
    - terminator: The jump instruction ending this block (if any)
    - successors: List of successor blocks (outgoing edges)
    - predecessors: List of predecessor blocks (incoming edges)
    """
    
    def __init__(self, block_id: int):
        self.id = block_id
        self.label: Optional[str] = None
        self.instructions: List[Instruction] = []
        self.terminator: Optional[Instruction] = None  # IRJump or IRCondJump
        self.successors: List['BasicBlock'] = []
        self.predecessors: List['BasicBlock'] = []
    
    def add_instruction(self, instr: Instruction):
        """Add an instruction to this block."""
        self.instructions.append(instr)
    
    def set_terminator(self, instr: Instruction):
        """Set the terminating jump instruction."""
        self.terminator = instr
    
    def add_successor(self, block: 'BasicBlock'):
        """Add a successor block and update bidirectional edges."""
        if block not in self.successors:
            self.successors.append(block)
        if self not in block.predecessors:
            block.predecessors.append(self)
    
    def __str__(self):
        """Pretty-print the basic block with proper formatting."""
        lines = []
        
        # Print label if exists
        if self.label:
            lines.append(f"{self.label}:")
        
        # Print instructions with indentation
        for instr in self.instructions:
            lines.append(f"    {instr}")
        
        # Print terminator if exists
        if self.terminator:
            lines.append(f"    {self.terminator}")
        
        return '\n'.join(lines)
    
    def __repr__(self):
        return f"BasicBlock(id={self.id}, label={self.label}, instrs={len(self.instructions)})"


# =======================
# Control Flow Graph
# =======================

class ControlFlowGraph:
    """Control Flow Graph consisting of basic blocks."""
    
    def __init__(self, blocks: List[BasicBlock]):
        self.blocks = blocks
        self.entry_block = blocks[0] if blocks else None
        self.linear_ir: List[Instruction] = []  # LABEL version (expression splitting phase)
        self.bb_ir: List[Instruction] = []      # BB version (basic block phase)
    
    def __str__(self):
        """Print all blocks in order (using BB version)."""
        if self.bb_ir:
            # Use BB version instructions
            lines = []
            for instr in self.bb_ir:
                if isinstance(instr, IRLabel):
                    lines.append(f"{instr.name}:")
                else:
                    lines.append(f"    {instr}")
            return '\n'.join(lines)
        else:
            # Fallback to original method
            result = []
            for block in self.blocks:
                block_str = str(block)
                if block_str:
                    result.append(block_str)
            return '\n'.join(result)
    
    def print_blocks_structure(self):
        """Print basic block structure - using BB_ labels.
        
        Basic block phase: Blocks are divided by BB_ labels.
        """
        print("=" * 80)
        print("Phase 2: Basic Blocks (with BB)")
        print("=" * 80)
        print()
        self._print_instructions(self.bb_ir)
        print()
    
    def print_linear_ir(self):
        """Print linear intermediate representation (Linear IR) - expression splitting phase.
        
        Uses LABEL_ labels.
        """
        print("=" * 80)
        print("Phase 1: Expression Splitting (Linear IR with LABEL)")
        print("=" * 80)
        print()
        self._print_instructions(self.linear_ir)
        print()
    
    def _print_instructions(self, instructions):
        """Print instruction list."""
        for instr in instructions:
            if isinstance(instr, IRLabel):
                print(f"{instr.name}:")
            else:
                print(f"    {instr}")
    
    def print_graph_info(self):
        """Print CFG structure information (for debugging)."""
        print(f"Control Flow Graph with {len(self.blocks)} blocks:")
        print(f"Entry block: {self.entry_block.id if self.entry_block else 'None'}")
        print()
        for block in self.blocks:
            print(f"Block {block.id} (label: {block.label or 'None'}):")
            print(f"  Instructions: {len(block.instructions)}")
            print(f"  Successors: {[b.id for b in block.successors]}")
            print(f"  Predecessors: {[b.id for b in block.predecessors]}")
            print()
    
    def to_mermaid(self) -> str:
        """Generate Mermaid flowchart.
        
        Features:
        - Conditional statements represented as diamond shapes
        - Basic blocks contain only regular instructions (no jumps)
        - Display full instructions without truncation
        """
        lines = ["flowchart TD"]
        
        # Generate nodes for each block
        for block in self.blocks:
            block_id = f"B{block.id}"
            
            # Show only regular instructions (no jumps)
            if block.instructions:
                content = []
                for instr in block.instructions:
                    instr_str = str(instr)
                    # Escape special characters (only quotes and &)
                    instr_str = instr_str.replace('"', "'")
                    instr_str = instr_str.replace('&', '&amp;')
                    content.append(instr_str)
                
                # Join with <br/>
                content_str = "<br/>".join(content)
                
                # Rectangle node (regular basic block)
                lines.append(f'    {block_id}["{content_str}"]')
            else:
                # Empty block
                lines.append(f'    {block_id}["(empty)"]')
            
            # If there's a conditional jump, create diamond decision node
            if isinstance(block.terminator, IRCondJump):
                cond_id = f"C{block.id}"
                cond = block.terminator.cond
                # Escape special characters (only &, < > can remain in condition)
                cond = cond.replace('&', '&amp;')
                # Diamond node (single curly braces)
                lines.append(f'    {cond_id}{{{cond}}}')
        
        lines.append("")
        
        # Generate edges
        for block in self.blocks:
            block_id = f"B{block.id}"
            
            if isinstance(block.terminator, IRCondJump):
                # Conditional jump: basic block -> diamond -> true/false branches
                cond_id = f"C{block.id}"
                lines.append(f"    {block_id} --> {cond_id}")
                
                # False branch: jump to target
                target_label = block.terminator.label
                false_target = None
                for b in self.blocks:
                    if b.label == target_label:
                        false_target = b
                        break
                
                # True branch: fall-through to next block
                true_target = None
                if len(block.successors) == 2:
                    for succ in block.successors:
                        if succ != false_target:
                            true_target = succ
                            break
                
                if false_target:
                    lines.append(f"    {cond_id} -->|false| B{false_target.id}")
                if true_target:
                    lines.append(f"    {cond_id} -->|true| B{true_target.id}")
                
            elif isinstance(block.terminator, IRJump):
                # Unconditional jump: direct connection
                target_label = block.terminator.label
                for b in self.blocks:
                    if b.label == target_label:
                        lines.append(f"    {block_id} --> B{b.id}")
                        break
            else:
                # No jump: fall-through
                if block.successors:
                    for succ in block.successors:
                        lines.append(f"    {block_id} --> B{succ.id}")
                elif not block.successors:
                    # Exit
                    lines.append(f"    {block_id} --> Exit([Exit])")
        
        # Styles
        lines.append("")
        if self.entry_block:
            lines.append(f"    style B{self.entry_block.id} fill:#e1f5e1")
        lines.append("    style Exit fill:#ffe1e1")
        
        return "\n".join(lines)
    
    def save_mermaid(self, filename: str):
        """Save Mermaid diagram to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("```mermaid\n")
            f.write(self.to_mermaid())
            f.write("\n```\n")
        print(f"Mermaid diagram saved to: {filename}")

