# ChromaKeying
Developed a real-time green screen matting system using OpenCV to apply chroma key effects, replacing selected color regions in videos with custom backgrounds. This technique is routinely used in the movie and television industry to replace the background of the actor, newscaster, or weatherman.
A video or live feed of a subject (actor) is shot in front of a solid green screen. Based on the color, the green screen is removed with an interesting background in post production or in real time.
Input: The input to the algorithm will be a video with a subject in front of a green screen.
Output: The output should be another video where the green background is replaced with an interesting background of your choice.
Controls: You can build a simple interface using HighGUI. It should contain the following parts.

Color Patch Selector : The interface should show a video frame and the user should be allowed to select a patch of green screen from the background. For simplicity, this patch can be a rectangular patch selected from a single frame. However, it is perfectly find to build an interface where you select multiple patches from one or more frames of the video.

Tolerance slider : This slider will control how different the color can be from the mean of colors sampled in the previous step to be included in the green background.

Softness slider (Optional): This slider will control the softness of the foreground mask at the edges.

Color cast slider (Optional): In a green screen environment, some of the green color also gets cast on the subject. There are some interesting ways the color cast can be reduced, but during the process of removing the color cast some artifacts are get introduced. So, this slider should control the amount of color cast removal we want.

Implementation:
1.Implemented dynamic color selection using mouse interaction, allowing users to define regions of interest for background replacement based on specific color tolerance.
2.Created a system that utilized trackbars to adjust chroma key parameters such as color tolerance, softness (Gaussian blur), and green cast removal, enhancing the flexibility of visual effects.
3.Optimized image processing workflows, including smoothing (Gaussian blur) of foreground elements to achieve seamless merging between subject and background.
4.Applied bitwise operations to generate masks and overlays, extracting foreground regions while suppressing green-screen regions, ensuring accurate and high-quality video compositing.
5.Extended the system to support video frame processing, enabling smooth real-time application of chroma key effects across entire video streams.
6.Achieved efficient real-time performance with the integration of functions for resizing frames, applying filters, and dynamically adjusting visual parameters, ensuring optimal results during live video feed manipulation.
7.Incorporated background resizing and enhancement techniques to align with foreground subjects and remove unwanted color casts, improving the overall aesthetic quality of the video output.

