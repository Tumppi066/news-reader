print("Importing modules...")
from summary import get_summary_for
from speech import play_audio_for
from rss import get_feed_for

feed = get_feed_for(24)
text = get_summary_for(feed)
play_audio_for(text)