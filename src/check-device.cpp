#pragma comment(lib, "k4a.lib")
#include <k4a/k4a.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "assert.h"

long WriteToFile(const char *fileName, void *buffer, size_t bufferSize)
{
    assert(buffer != NULL);

    std::ofstream hFile;
    hFile.open(fileName, std::ios::out | std::ios::trunc | std::ios::binary);
    if (hFile.is_open())
    {
        hFile.write((char *)buffer, static_cast<std::streamsize>(bufferSize));
        hFile.close();
    }
    //std::cout << "[Streaming Service] Color frame is stored in " << fileName << std::endl;

    return 0;
}

int main(int argc,char* argv[])
{
    std::string fps, color, resolution, depth, unix_time;
    if(argc >= 2){
      fps = argv[2];
      color = argv[4];
      resolution = argv[6];
      depth = argv[8];
      unix_time = argv[10];
      printf("K4A Image config: \nfps: %s, color: %s, resolution: %s, depth: %s\n", fps.c_str(), color.c_str(), resolution.c_str(), depth.c_str());
    }
    uint32_t count = k4a_device_get_installed_count();
    k4a_capture_t capture = NULL;
    int returnCode = 1;
    const int32_t TIMEOUT_IN_MS = 1000;

    if (count == 0)
    {
        printf("\nNo k4a devices attached!\n");
        return 1;
    }

    // Open the first plugged in Kinect device
    k4a_device_t device = NULL;
    if (K4A_FAILED(k4a_device_open(K4A_DEVICE_DEFAULT, &device)))
    {
        printf("Failed to open k4a device!\n");
        return 1;
    }

    // Get the size of the serial number
    size_t serial_size = 0;
    k4a_device_get_serialnum(device, NULL, &serial_size);

    // Allocate memory for the serial, then acquire it
    char *serial = (char*)(malloc(serial_size));
    k4a_device_get_serialnum(device, serial, &serial_size);
    printf("Opened device: %s\n", serial);
    free(serial);

    // Set cameras default settings
    k4a_device_configuration_t config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    config.camera_fps       = K4A_FRAMES_PER_SECOND_15;
    config.color_format     = K4A_IMAGE_FORMAT_COLOR_BGRA32;
    config.color_resolution = K4A_COLOR_RESOLUTION_1080P;
    config.depth_mode = K4A_DEPTH_MODE_NFOV_2X2BINNED;

    // Set cameras settings based on cmd args
    if(fps=="5")
      config.camera_fps       = K4A_FRAMES_PER_SECOND_5;
    else if(fps=="15")
      config.camera_fps       = K4A_FRAMES_PER_SECOND_15;
    else if(fps=="30")
      config.camera_fps       = K4A_FRAMES_PER_SECOND_15;

    if(color=="MJPG")
      config.color_format     = K4A_IMAGE_FORMAT_COLOR_MJPG;
    else if(color=="NV12")
      config.color_format     = K4A_IMAGE_FORMAT_COLOR_NV12;
    else if(color=="YUY2")
      config.color_format     = K4A_IMAGE_FORMAT_COLOR_YUY2;
    else if(color=="BGRA32")
      config.color_format     = K4A_IMAGE_FORMAT_COLOR_BGRA32;
    else if(color=="DEPTH16")
      config.color_format     = K4A_IMAGE_FORMAT_DEPTH16;
    else if(color=="IR16")
      config.color_format     = K4A_IMAGE_FORMAT_IR16;

    if(resolution=="OFF")
      config.color_resolution     = K4A_COLOR_RESOLUTION_OFF;
    else if(resolution=="720P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_720P;
    else if(resolution=="1080P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_1080P;
    else if(resolution=="1440P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_1440P;
    else if(resolution=="1536P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_1536P;
    else if(resolution=="2160P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_2160P;
    else if(resolution=="3072P")
      config.color_resolution     = K4A_COLOR_RESOLUTION_3072P;

    if(depth=="OFF")
      config.depth_mode     = K4A_DEPTH_MODE_OFF;
    else if(depth=="NFOV_2X2BINNED")
      config.depth_mode     = K4A_DEPTH_MODE_NFOV_2X2BINNED;
    else if(depth=="NFOV_UNBINNED")
      config.depth_mode     = K4A_DEPTH_MODE_NFOV_UNBINNED;
    else if(depth=="WFOV_2X2BINNED")
      config.depth_mode     = K4A_DEPTH_MODE_WFOV_2X2BINNED;
    else if(depth=="WFOV_UNBINNED")
      config.depth_mode     = K4A_DEPTH_MODE_WFOV_UNBINNED;
    else if(depth=="PASSIVE_IR")
      config.depth_mode     = K4A_DEPTH_MODE_PASSIVE_IR;

    // Start the camera with the given configuration
    if (K4A_FAILED(k4a_device_start_cameras(device, &config)))
    {
        printf("Failed to start cameras!\n");
        k4a_device_close(device);
        return 1;
    }
    int captureFrameCount = 3;
    // Camera capture and application specific code would go here
        while (captureFrameCount-- > 0)
    {
        k4a_image_t image;

        // Get a depth frame
        switch (k4a_device_get_capture(device, &capture, TIMEOUT_IN_MS))
        {
        case K4A_WAIT_RESULT_SUCCEEDED:
            break;
        case K4A_WAIT_RESULT_TIMEOUT:
            printf("Timed out waiting for a capture\n");
            continue;
            break;
        case K4A_WAIT_RESULT_FAILED:
            printf("Failed to read a capture\n");
            goto Exit;
        }

        printf("Capture");

        // Probe for a color image
        image = k4a_capture_get_color_image(capture);
        if (image)
        {
            printf(" | Color res:%4dx%4d stride:%5d ",
                   k4a_image_get_height_pixels(image),
                   k4a_image_get_width_pixels(image),
                   k4a_image_get_stride_bytes(image));
                   WriteToFile("color_data. jpeg", k4a_image_get_buffer( image ), k4a_image_get_size(image));
            k4a_image_release(image);
        }
        else
        {
            printf(" | Color None                       ");
        }

        // probe for a IR16 image
        image = k4a_capture_get_ir_image(capture);
        if (image != NULL)
        {
            printf(" | Ir16 res:%4dx%4d stride:%5d ",
                   k4a_image_get_height_pixels(image),
                   k4a_image_get_width_pixels(image),
                   k4a_image_get_stride_bytes(image));
                   WriteToFile("ir16_data", k4a_image_get_buffer( image ), k4a_image_get_size(image));
            k4a_image_release(image);
        }
        else
        {
            printf(" | Ir16 None                       ");
        }

        // Probe for a depth16 image
        image = k4a_capture_get_depth_image(capture);
        if (image != NULL)
        {
            printf(" | Depth16 res:%4dx%4d stride:%5d\n",
                   k4a_image_get_height_pixels(image),
                   k4a_image_get_width_pixels(image),
                   k4a_image_get_stride_bytes(image));
                   WriteToFile("depth16_data", k4a_image_get_buffer( image ), k4a_image_get_size(image));
            k4a_image_release(image);
        }
        else
        {
            printf(" | Depth16 None\n");
        }

        // release capture
        k4a_capture_release(capture);
        fflush(stdout);
    }
    // Shut down the camera when finished with application logic
    k4a_device_stop_cameras(device);
    k4a_device_close(device);

    return 0;

    returnCode = 0;
    Exit:
    if (device != NULL)
    {
        k4a_device_close(device);
    }

    return returnCode;
}
