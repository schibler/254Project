; Function to add two integers
define i32 @add_two_numbers(i32 %a, i32 %b) {
entry:
  ; Add the integers %a and %b, and store the result in %sum
  %sum = add i32 %a, %b
  ; Return the result (%sum)
  ret i32 %sum
}

; Main function
define i32 @main() {
entry:
  ; Declare local variables
  %x = alloca i32, align 4
  %y = alloca i32, align 4

  ; Store the values 5 and 7 into %x and %y
  store i32 5, i32* %x, align 4
  store i32 7, i32* %y, align 4

  ; Load the values from %x and %y
  %a = load i32, i32* %x, align 4
  %b = load i32, i32* %y, align 4

  ; Call the function add_two_numbers with %a and %b as arguments
  %result = call i32 @add_two_numbers(i32 %a, i32 %b)

  ; Return the result
  ret i32 %result
}

