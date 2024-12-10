//===-- HelloWorld.cpp - Example Transformations --------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#include "llvm/Transforms/Utils/HelloWorld.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/InstrTypes.h"

#include <map>
#include <utility>
#include <string>

using namespace llvm;

PreservedAnalyses HelloWorldPass::run(Function &F,
                                      FunctionAnalysisManager &AM) {
  errs() << F.getName() << "\n";
  std::map<std::string, int> colors;
  std::map<std::pair<std::string, std::string>, int> edges;
  std::map<const Instruction*, std::string> instNames;
  int counter = 1;
  for(auto &BB : F) {
    for(auto &inst : BB) {
      std::string name = "inst" + std::to_string(counter++);
      int color = 0;
      if(isa<LoadInst>(inst) || isa<StoreInst>(inst)) {
        color = 1;
      } else if(isa<BinaryOperator>(inst)) {
        if((inst.getOpcode() == Instruction::FAdd) || (inst.getOpcode() == Instruction::FSub) || (inst.getOpcode() == Instruction::FMul) || (inst.getOpcode() == Instruction::FDiv) || (inst.getOpcode() == Instruction::FRem)) {
          color = 2;
        }
      }
      colors[name] = color;
      instNames[&inst] = name;
      for (auto &Op : inst.operands()) {
        if(auto *OpInst = dyn_cast<Instruction>(Op)) {
          if(isa<LoadInst>(OpInst) || isa<StoreInst>(OpInst)) {
	    edges[{instNames[OpInst], name}] = 3;
	  } else if ((OpInst->getOpcode() == Instruction::FAdd) || (OpInst->getOpcode() == Instruction::FSub) || (OpInst->getOpcode() == Instruction::FMul) || (OpInst->getOpcode() == Instruction::FDiv) || (OpInst->getOpcode() == Instruction::FRem)) {
	    edges[{instNames[OpInst], name}] = 4;
	  } else {
	    edges[{instNames[OpInst], name}] = 1;
	  }
        }
      }
    }
  }
  errs() << "digraph G {\n";
  for (auto keyval : colors) {
    std::string inst = keyval.first;
    int color = keyval.second;
    if(color == 1) {
      errs() << "  " << inst << " [color=\"red\"];\n";
    } else if(color == 2) {
      errs() << "  " << inst << " [color=\"yellow\"];\n";
    } else {
      errs() << "  " << inst << " [color=\"blue\"];\n";
    }
  }
  for(auto keyval : edges) {
    std::string u = keyval.first.first;
    std::string v = keyval.first.second;
    int weight = keyval.second;
    // errs() << "  " << u << " -> " << v << " [weight=" << weight << "];\n";
    errs() << "  " << u << " -> " << v << " [weight=" << weight << " label=\"" << weight << "\"];\n";
  }
  errs() << "}\n";
  return PreservedAnalyses::all();
}
