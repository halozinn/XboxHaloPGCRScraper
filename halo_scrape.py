import logging, sys
import argparse
from PIL import Image
import pytesseract
import cv2
import utils

def process_video(path, logger):
    logger.info("processing input from device {}".format(path))
    #pass video argument into cv2
    vidcap = cv2.VideoCapture(path)
    #get video file info
    count = 0
    success,image = vidcap.read()
    pgcr_flag = 0
    logger.debug("Reading capture now. Force quit to stop.")

    while success:
        #increment video by one second, then read frame
        count+=1
        success,image = vidcap.read()
        # avoid all but 1 in 30 frames
        if count % 30 != 0:
            continue
        #if the text we are looked for is there, save screenshot with video timestamp
        if pgcr_flag == 0:
            ok, text = utils.is_pgcr(image)
            if not ok:
                continue
            logger.debug(text)
            red_score, blue_score = utils.get_scores(image, logger)
            logger.info("red_score: {} blue_score: {}".format(red_score, blue_score))
            minutes = int(count/60)
            seconds = count % 60
            logger.debug("PGCR Present at frame " + str(count))
            cv2.imwrite(str(minutes) + "_" + str(seconds) + ".png", image)
            pgcr_flag = 1
        #to prevent screenshotting the same PGCR potentially hundreds of times, use this flag prevent that
        else:
            ok, text = utils.is_pgcr(image)
            if ok:
                continue
            pgcr_flag = 0

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    logger = logging.getLogger("halo_scrape")
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("-v",
            "--video",
            required=False,
            help="path to input video")
    group.add_argument("-i",
            "--index",
            required=False,
            help="index of device to capture video from")
    group.add_argument("--image",
            required=False,
            help="path to image to check for winner")

    ap.add_argument("--version",
            action='version',
            version='0.1')
    ap.add_argument("--debug",
            action="store_true",
            help="enable debug logging")

    args = ap.parse_args()
    # enable debug logging
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug("args: {}".format(args))
    if args.video != None:
        process_video(args.video, logger)
    elif args.index != None:
        process_video(args.index, logger)
    else:
        image = cv2.imread(args.image)
        red_score, blue_score = utils.get_scores(image, logger)
        print("red: {}, blue: {}".format(red_score, blue_score))


if __name__ == "__main__":
    main()
