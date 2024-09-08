#include <pybind11/pybind11.h>
#include <LoopbackCapture.h>
#include <iostream>
#include <windows.h>
#include <signal.h>
#include <Python.h>
#include <pathcch.h>

#include "FindProcess.cpp"

#pragma comment(lib, "Pathcch.lib")

namespace py = pybind11;

CLoopbackCapture loopbackCapture;
HANDLE ctrlCEvent;
HRESULT hr;

BOOL WINAPI ConsoleCtrlHandler(DWORD dwCtrlType) {
    switch (dwCtrlType) {
    case CTRL_C_EVENT:
        SetEvent(ctrlCEvent);
        return TRUE;
    default:
        return FALSE;
    }
}


std::wstring record(wchar_t* procname, int duration, wchar_t* output_dir ) {
    
    int pid = findProc(prepare_name(procname).c_str());
    
    ctrlCEvent = CreateEvent(NULL, TRUE, FALSE, NULL);  // Manual reset, initially unsignaled
    if (ctrlCEvent == NULL) {
        printf("ERROR: Could not create event!\n");
        return std::wstring(L"");
    }

    // Set the control handler for the console
    if (!SetConsoleCtrlHandler(ConsoleCtrlHandler, TRUE)) {
        printf("ERROR: Could not set control handler!\n");
        return std::wstring(L"");
    }

    BOOL yo = CreateDirectory(output_dir, NULL);
    wchar_t path_to_wav[MAX_PATH];
    hr = PathCchCombineEx(path_to_wav, MAX_PATH, output_dir, L"popo.wav", 0);
    hr = loopbackCapture.StartCaptureAsync(pid, true, path_to_wav);

    if (FAILED(hr))
    {
        wil::unique_hlocal_string message;
        FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_ALLOCATE_BUFFER, nullptr, hr,
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (PWSTR)&message, 0, nullptr);
        std::wcout << L"Failed to start capture\n0x" << std::hex << hr << L": " << message.get() << L"\n";
    }
    else
    {
        std::wcout << L"Capturing audio, press Ctrl+C to stop recording..." << std::endl;

        // Wait for the event to be signaled by the Ctrl+C handler

        if (duration) WaitForSingleObject(ctrlCEvent, duration*1000*60);
        else WaitForSingleObject(ctrlCEvent, INFINITE);

        loopbackCapture.StopCaptureAsync();
        std::wcout << L"Stopped recording!" << std::endl;
        // Clean up the event object
        CloseHandle(ctrlCEvent);
    }

    std::wstring path_str(path_to_wav);
    return path_str;
}

PYBIND11_MODULE(record, m) {
    m.doc() = ""; // optional module docstring

    m.def("record", &record);
}