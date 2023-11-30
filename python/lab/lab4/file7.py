def search(*files, word):
    for file in files:
        f = open(f"{file}.txt")
        fw = open("write7.txt", "a")
        content = f.readlines()
        for i in range(len(content)):
           if word in content[i]:
               fw.write(f"{str([file, i])}\n")



search("text7", "text8", word="word")