# 254Project

## Replicating our LLVM Build
1. Checkout LLVM using `$ git clone https://github.com/llvm/llvm-project.git` or

    `$ git clone --depth 1 https://github.com/llvm/llvm-project.git` (for a shallow clone)

2. [Download](http://www.cmake.org/cmake/resources/software.html) and install CMake. Version 3.20.0 is the minimum required.

3. Install ninja.

   `$ pip install ninja`

5. Create a build directory. Building LLVM in the source directory is not supported. cd to this directory:
   ```
   $ mkdir mybuilddir
   $ cd mybuilddir
   ```
6. Execute this command in the shell replacing path/to/llvm/source/root with the path to the root of your LLVM source tree:

   `$ cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug path/to/llvm/source/root`
   
### To Run a Pass with `opt`
In the build directory, run the following commands:
   ```
   $ ninja opt
   $ bin/opt -disable-output ../a.ll -passes=helloworld > output.dot
   ```

The results of the pass should be printed to `output.dot`
