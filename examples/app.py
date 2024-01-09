# pylint: disable=missing-function-docstring

from refinery import Bucket, function
from refinery.queue import Queue, ReceivedMessagesEvent
from refinery.synth import synth


video_queue = Queue[str]("video_queue", fifo=True)

files = Bucket("files")

videos = files / "videos"


@video_queue.on("create")
async def process_video_(event: ReceivedMessagesEvent[str]):
    pass


@videos.on("create")
async def process_video(event: Bucket.ObjectCreatedEvent):
    await video_queue.send(event.key)


@function()
async def upload_video():
    await upload("key", "data")


async def upload(key: str, file: str):
    await videos.put(key, file)


if __name__ == "__main__":
    spec = synth()
    print(spec.model_dump_json(indent=2))
