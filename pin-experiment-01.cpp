#include "pin.H"
#include <iostream>
#include <string>

// Global variable to store the command line arguments
char** g_argv;
int g_argc;

// Function to be called before main
VOID BeforeMain(CHAR** argv, INT argc)
{
    g_argv = argv;
    g_argc = argc;

    // Check if there is at least one command line argument
    if (argc > 1)
    {
        std::string arg1 = argv[1];
        if (arg1 == "2")
        {
            std::cerr << "argv[1] is equal to 2" << std::endl;
        }
    }
}

// Instrumentation function
VOID ImageLoad(IMG img, VOID* v)
{
    // Check if the loaded image is the application itself
    if (IMG_IsMainExecutable(img))
    {
        // Get the main routine's RTN
        RTN mainRtn = RTN_FindByName(img, "main");
        if (RTN_Valid(mainRtn))
        {
            // Insert call to BeforeMain before the main function
            RTN_InsertCall(mainRtn, IPOINT_BEFORE, (AFUNPTR)BeforeMain,
                           IARG_CMD_LINE_ARGV, IARG_CMD_LINE_ARGC,
                           IARG_END);
        }
    }
}

// Pin calls this function when the application exits
VOID Fini(INT32 code, VOID* v)
{
    // Nothing to do here for this example
}

int main(int argc, char* argv[])
{
    // Initialize Pin
    PIN_Init(argc, argv);

    // Register ImageLoad to be called when an image is loaded
    IMG_AddInstrumentFunction(ImageLoad, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);

    // Start the program, never returns
    PIN_StartProgram();

    return 0;
}