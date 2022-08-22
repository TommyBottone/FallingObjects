from ImageReader import ImageMetaData

metadata = ImageMetaData()
samplename = "./samples/lg3_outline.jpg"


def main():
    metadata.readImage(samplename)
    return


if __name__ == "__main__":
    main()
