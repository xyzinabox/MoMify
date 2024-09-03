#pragma once

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tlhelp32.h>
#include <iostream>
#include <psapi.h>
#include <shlwapi.h>
#include <string>
#include <algorithm>

#pragma comment(lib, "Shlwapi.lib")


std::wstring prepare_name(wchar_t* name) {
    int err = _wcslwr_s(name, wcslen(name)+1);
    std::wstring _name(name);
    if (_name.size() >= 4 && _name.compare(_name.size() - 4, 4, L".exe")) _name.append(L".exe");
    
    return _name;
}

// find process ID by process name
int findProc(const wchar_t* procname) {

    HANDLE hSnapshot;
    PROCESSENTRY32 pe;
    int current_pid, parent_pid;
    int potential_pid = 0;
    int backup_potential_pid = 0;
    BOOL hResult;

    // snapshot of all processes in the system
    hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (INVALID_HANDLE_VALUE == hSnapshot) return 0;

    // initializing size: needed for using Process32First
    pe.dwSize = sizeof(PROCESSENTRY32);

    // info about first process encountered in a system snapshot
    hResult = Process32First(hSnapshot, &pe);

    // retrieve information about the processes
    // and exit if unsuccessful
    while (hResult) {
        // if we find the process: return process ID
        if (wcscmp(procname, prepare_name(pe.szExeFile).c_str()) == 0) {

            current_pid = pe.th32ProcessID;
            parent_pid = pe.th32ParentProcessID;
            if (potential_pid == current_pid) {
                return current_pid;
            }
            else if (backup_potential_pid) {
                hResult = Process32Next(hSnapshot, &pe);
                continue;
            }
            // handle = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, false, parent_pid);
            // wchar_t Buffer[MAX_PATH];
            // if (GetProcessImageFileName(handle, Buffer, MAX_PATH) == 0) {
            //     int error = GetLastError()
            //     std::cout << "Could not open parent process while searching. Aborting..." << std::endl;
            // }

            // if (wcscmp(procname, PathFindFileName(Buffer))) {
            //     CloseHandle(handle);
            //     CloseHandle(hSnapshot);
            //     return current_pid;
            // }
            potential_pid = parent_pid;
            backup_potential_pid = current_pid;
        }
        hResult = Process32Next(hSnapshot, &pe);
    }

    // closes an open handle (CreateToolhelp32Snapshot)
    CloseHandle(hSnapshot);
    return backup_potential_pid;
}
