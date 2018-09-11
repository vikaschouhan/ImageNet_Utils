#!/usr/bin/env python
import argparse
import sys
import os
import _init_paths
import imagedownloader
import pref_utils

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Help the user to download, crop, and handle images from ImageNet')
    p.add_argument('--wnid', help='ImageNet Wnids separated by comma. E.g. : n02710324')
    p.add_argument('--downloadImages', help='Should download images', action='store_true', default=False)
    p.add_argument('--downloadOriginalImages', help='Should download original images', action='store_true', default=False)
    p.add_argument('--downloadBoundingBox', help='Should download bouding box annotation files', action='store_true', default=False)
    # p.add_argument('--jobs', '-j', type=int, default=1, help='Number of parallel threads to download')
    # p.add_argument('--timeout', '-t', type=int, default=10, help='Timeout per image in seconds')
    # p.add_argument('--retry', '-r', type=int, default=10, help='Max count of retry for each image')
    p.add_argument('--verbose', '-v', action='store_true', help='Enable verbose log')
    p.add_argument('--numberOfImages', help='Number of images for this wnid', type=int, default=None)
    args = p.parse_args()
    if args.wnid is None:
        print 'No wnid'
        sys.exit()

    downloader = imagedownloader.ImageNetDownloader()
    username = None
    accessKey = None
    userInfo = pref_utils.readUserInfo()
    if not userInfo is None:
        username = userInfo[0]
        accessKey = userInfo[1]

    wnid_l = args.wnid.replace(' ', '').split(',')

    if args.downloadImages is True:
        for id in wnid_l:
            print('Downloading {} images for {}'.format(args.numberOfImages if args.numberOfImages else 'all', id))
            list = downloader.getImageURLsOfWnid(id)
            list = list[0:args.numberOfImages+1] if args.numberOfImages else list
            downloader.downloadImagesByURLs(id, list)

    if args.downloadBoundingBox is True:
        for id in wnid_l:
            # Download annotation files
            downloader.downloadBBox(id)

    if args.downloadOriginalImages is True:
    # Download original image, but need to set key and username
        if username is None or accessKey is None:
            username = raw_input('Enter your username : ')
            accessKey = raw_input('Enter your accessKey : ')
            if username and accessKey:
                pref_utils.saveUserInfo(username, accessKey)

        if username is None or accessKey is None:
            print 'need username and accessKey to download original images'
        else:
            for id in wnid_l:
                downloader.downloadOriginalImages(id, username, accessKey)
