.data
    fileNameRead: .asciz "in.txt"
    fileNameWrite: .asciz "out.txt"
    modeRead: .asciz "r"
    modeWrite: .asciz "w"
    fileHandleRead: .long 0
    fileHandleWrite: .long 0
    formatScanf: .asciz "%ld"
    formatPrintf: .asciz "%ld" 
    buffer: .space 4
    buffer2: .space 4

.text
.global main
main:
    # Open the file
    push $modeRead
    push $fileNameRead
    call fopen
    mov %eax, fileHandleRead
    add $8, %esp  
  
    push $modeWrite
    push $fileNameWrite
    call fopen
    mov %eax, fileHandleWrite
    add $8, %esp 
    
    
    lea buffer, %eax 
    push %eax
    push $formatScanf
    push fileHandleRead
    call fscanf
    add $12, %esp  # Adjust the stack after the call


    push buffer
    push $formatPrintf
    push fileHandleWrite
    call fprintf
    add $12, %esp

    push fileHandleRead
    call fclose
    add $4, %esp 

    push fileHandleWrite
    call fclose
    add $4, %esp 

exit:
    mov $1, %eax
    xor %ebx, %ebx
    int $0x80
