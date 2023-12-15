#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

int main()
{
    for (int i = 1; i <= 50; ++i)
    {
        std::ostringstream filenameStream;
        filenameStream << "file_" << i << ".txt";
        std::string filename = filenameStream.str();

        std::ofstream outfile(filename);
        if (outfile.is_open())
            outfile.close();
    }
}
