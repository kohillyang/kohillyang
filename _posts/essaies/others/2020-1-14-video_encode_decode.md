---
layout: post
title: 视频编码解码
date: 2020-1-14 19:40
comments: true 
external-url:
categories: linux
permalink: /video_encoding_and_decoding
---
<br>

An encoder sends an IDR (Instantaneous Decoder Refresh) coded picture (made up of I- or SI-slices) to clear the contents of the reference picture buffer. On receiving an IDR coded picture, the decoder marks all pictures in the reference buffer as ‘unused for reference’. All subsequent transmitted slices can be decoded without reference to any frame decoded prior to the IDR picture. The first picture in a coded video sequence is always an IDR picture.

IDR-Frame clears the reference picture buffer, i.e. no frame after IDR can reference any frame before IDR. That's not the case with "normal" I-Frame, i.e. P- or B-Frame after I-Frame can use as reference frames before I-Frame. I-frame is a short for intraframe, a video compression method used by the MPEG standard. Every IDR frame is an I-frame, but not vice versa; so there can be I-frames that aren’t IDR frames.

Refrence Book:
<https://www.amazon.com/H-264-MPEG-4-Video-Compression-Generation/dp/0470848375/ref=sr_1_2?s=books&ie=UTF8&qid=1325020249&sr=1-2>
<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-14-00-03-04.png" class="img-responsive" style="width:20%;margin-left:2%"/><br>

About NAL units(From [wiki](https://en.wikipedia.org/wiki/Network_Abstraction_Layer)):

The NAL is designed in order to provide "network friendliness" to enable simple and effective customization of the use of VCL for a broad variety of systems. The NAL facilitates the ability to map VCL data to transport layers such as:[1]
```
    RTP/IP for any kind of real-time wire-line and wireless Internet services.[1]
    File formats, e.g., ISO MP4 for storage and MMS.[1]
    H.32X for wireline and wireless conversational services.[1]
    MPEG-2 systems for broadcasting services, etc.[1]
```
[1]: [Overview of the H.264/AVC Video Coding Standard, IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS FOR VIDEO TECHNOLOGY, VOL. 13, NO. 7, JULY 2003](http://ip.hhi.de/imagecom_G1/assets/pdfs/csvt_overview_0305.pdf)




