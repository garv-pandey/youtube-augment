# TODO: add shorts urls

YT_VIDEOS = [
    {
        # technoblade potato war 2
        "url": "https://www.youtube.com/watch?v=0PAEqgfAts4",
        "video_id": "0PAEqgfAts4",
        "playlist_id": None,
    },
    {
        # ArhyBES batmetal
        "url": "https://www.youtube.com/watch?v=qatmJtIJAPw",
        "video_id": "qatmJtIJAPw",
        "playlist_id": None,
    },
    {
        # falshdeckanimations DE dust2
        "url": "https://www.youtube.com/watch?v=5Cjrp23lBSM&t=6s",
        "video_id": "5Cjrp23lBSM",
        "playlist_id": None,
    },
]

YT_PLAYLISTS = [
    {
        # technoblade potato war
        "url": "https://www.youtube.com/playlist?list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT",
        "video_id": None,
        "playlist_id": "PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT",
    },
    {
        # ArhyBES BATMETAL playlist
        "url": "https://www.youtube.com/playlist?list=PLJkYK-Q3rpa-3iebwyvEpkbGJnt8jJ1PU",
        "video_id": None,
        "playlist_id": "PLJkYK-Q3rpa-3iebwyvEpkbGJnt8jJ1PU",
    },
    {
        # falshdeckanimations CS animated series
        "url": "https://www.youtube.com/playlist?list=PLB27741DDE1240BEB",
        "video_id": None,
        "playlist_id": "PLB27741DDE1240BEB",
    },
]

YT_VIDEO_IN_PLAYLISTS = [
    {
        # technoblade potato war -> potato war 2
        "url": "https://www.youtube.com/watch?v=0PAEqgfAts4&list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT&index=2&t=36s",
        "video_id": "0PAEqgfAts4",
        "playlist_id": "PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT",
    },
    {
        # ArhyBES batmetal in BATMETAL playlist
        "url": "https://www.youtube.com/watch?v=qatmJtIJAPw&list=PLJkYK-Q3rpa-3iebwyvEpkbGJnt8jJ1PU&index=1",
        "video_id": "qatmJtIJAPw",
        "playlist_id": "PLJkYK-Q3rpa-3iebwyvEpkbGJnt8jJ1PU",
    },
    {
        # falshdeckanimations CS animated series -> CS DE dust2
        "url": "https://www.youtube.com/watch?v=5Cjrp23lBSM&list=PLB27741DDE1240BEB&index=2",
        "video_id": "5Cjrp23lBSM",
        "playlist_id": "PLB27741DDE1240BEB",
    },
]

# cant get solo link for mix playlists
# YT_MIX_PLAYLISTS = []

YT_VIDEO_IN_MIX_PLAYLISTS = [
    {
        # random mix
        "url": "https://www.youtube.com/watch?v=ZjPB3a2t1vk&list=RDZjPB3a2t1vk&start_radio=1",
        "video_id": "ZjPB3a2t1vk",
        "playlist_id": "RDZjPB3a2t1vk",
    },
    {
        # mix radio
        "url": "https://www.youtube.com/watch?v=Ua4WGK5SGHA&list=RDMM&start_radio=1&rv=ZjPB3a2t1vk",
        "video_id": "Ua4WGK5SGHA",
        "playlist_id": "RDMM",
    },
    {
        # another mix
        "url": "https://www.youtube.com/watch?v=kPkT0jMjEu8&list=RDkPkT0jMjEu8&start_radio=1&rv=Ua4WGK5SGHA",
        "video_id": "kPkT0jMjEu8",
        "playlist_id": "RDkPkT0jMjEu8",
    },
]

YT_SEASON_PLAYLISTS = [
    {
        # oversiplified punic war all episodes
        "url": "https://www.youtube.com/show/VLPLQw_XrMliWVa1cUis273NsyXIvH5DW6o2?season=AllEpisodes&sbp=CgtBbGxFcGlzb2RlcxoAKgt5Um1PV2NXZFFBb0AB",
        "video_id": None,
        "playlist_id": "PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2",
    },
    {
        # oversiplified punic war top episodes for you
        "url": "https://www.youtube.com/show/VLPLQw_XrMliWVa1cUis273NsyXIvH5DW6o2?season=TopEpisodesForYou&sbp=ChFUb3BFcGlzb2Rlc0ZvcllvdRoAKgt5Um1PV2NXZFFBb0AB",
        "video_id": None,
        "playlist_id": "PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2",
    },
    {
        # oversiplified world war all episodes
        "url": "https://www.youtube.com/show/VLPLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY?season=AllEpisodes&sbp=CgtBbGxFcGlzb2RlcxoAKgtkSFNRQUVhbTJ5Y0AB",
        "video_id": None,
        "playlist_id": "PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
    },
    {
        # oversiplified world war top episodes
        "url": "https://www.youtube.com/show/VLPLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY?season=TopEpisodesForYou&sbp=ChFUb3BFcGlzb2Rlc0ZvcllvdRoAKgtkSFNRQUVhbTJ5Y0AB",
        "video_id": None,
        "playlist_id": "PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
    },
]

YT_VIDEO_IN_SEASON_PLAYLISTS = [
    {
        # oversiplified punic war 1 part 1, present in all episodes and not in top episodes
        "url": "https://www.youtube.com/watch?v=yRmOWcWdQAo&list=PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2&t=16s",
        "video_id": "yRmOWcWdQAo",
        "playlist_id": "PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2",
    },
    {
        # oversiplified punic war 1 part 2 in top episodes
        "url": "https://www.youtube.com/watch_videos?video_ids=yRmOWcWdQAo%2ClsbcN9-jU1Y%2ChRSGxw2AQnk%2C1BVJzaXv3rk%2CQ-nWA0WeF98&type=0&title=Roman+History+%E2%80%A2+Top+episodes+for+you",
        "video_id": "yRmOWcWdQAo",
        "playlist_id": "PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2",
    },
    {
        # oversiplified punic war 1 part 2 in all episodes
        "url": "https://www.youtube.com/watch?v=hRSGxw2AQnk&list=PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2&t=29s",
        "video_id": "hRSGxw2AQnk",
        "playlist_id": "PLQw_XrMliWVa1cUis273NsyXIvH5DW6o2",
    },
    {
        # oversiplified world war 1 part 1, present in all episodes and not in top episodes
        "url": "https://www.youtube.com/watch?v=dHSQAEam2yc&list=PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
        "video_id": "dHSQAEam2yc",
        "playlist_id": "PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
    },
    {
        # oversiplified world war 1 part 2 in top episodes
        "url": "https://www.youtube.com/watch_videos?video_ids=dHSQAEam2yc%2CI79TpDe3t2g%2COIYy32RuHao%2CMun1dKkc_As%2Cfo2Rb9h788s%2C_uk_6vfqwTA&type=0&title=World+Wars+%E2%80%A2+Top+episodes+for+you",
        "video_id": "Mun1dKkc_As",
        "playlist_id": "PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
    },
    {
        # oversiplified world war 1 part 2 in all episodes
        "url": "https://www.youtube.com/watch?v=Mun1dKkc_As&list=PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY&t=136s",
        "video_id": "Mun1dKkc_As",
        "playlist_id": "PLQw_XrMliWVYdCBZ-ZJcv5nvUrjQPmjyY",
    },
]

YTM_VIDEOS = [
    {
        "url": "https://music.youtube.com/watch?v=mYBpnPd7g44",
        "video_id": "mYBpnPd7g44",
        "playlist_id": None,
    },
    {
        "url": "https://music.youtube.com/watch?v=Yl7TdNdTmpU",
        "video_id": "Yl7TdNdTmpU",
        "playlist_id": None,
    },
    {
        "url": "https://music.youtube.com/watch?v=QHRuTYtSbJQ",
        "video_id": "QHRuTYtSbJQ",
        "playlist_id": None,
    },
]

YTM_PLAYLISTS = [
    {
        "url": "https://music.youtube.com/playlist?list=PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt",
        "video_id": None,
        "playlist_id": "PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt",
    },
    {
        "url": "https://music.youtube.com/playlist?list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
        "video_id": None,
        "playlist_id": "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
    },
    {
        "url": "https://music.youtube.com/playlist?list=OLAK5uy_nuH6xdQMYiRKprzdS_hud6Y90NYDgcGYA",
        "video_id": None,
        "playlist_id": "OLAK5uy_nuH6xdQMYiRKprzdS_hud6Y90NYDgcGYA",
    },
]

YTM_VIDEO_IN_PLAYLISTS = [
    {
        "url": "https://music.youtube.com/watch?v=mYBpnPd7g44&list=PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt",
        "video_id": "mYBpnPd7g44",
        "playlist_id": "PLMlRYqqqM5rrjeaJuVaC6MWN7e7fSXGJt",
    },
    {
        "url": "https://music.youtube.com/watch?v=Yl7TdNdTmpU&list=PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
        "video_id": "Yl7TdNdTmpU",
        "playlist_id": "PLp9koScqE_BHhGcIrUuGmeCPRakLF-eY8",
    },
    {
        "url": "https://music.youtube.com/watch?v=QHRuTYtSbJQ&list=OLAK5uy_nuH6xdQMYiRKprzdS_hud6Y90NYDgcGYA",
        "video_id": "QHRuTYtSbJQ",
        "playlist_id": "OLAK5uy_nuH6xdQMYiRKprzdS_hud6Y90NYDgcGYA",
    },
]

YTM_MIX_PLAYLISTS = [
    {
        # create a mix
        "url": "https://music.youtube.com/playlist?list=RDATmba11fjz9y3mcE",
        "video_id": None,
        "playlist_id": "RDATmba11fjz9y3mcE",
    },
    {
        # suggested mix
        "url": "https://music.youtube.com/playlist?list=RDTMAK5uy_nilrsVWxrKskY0ZUpVZ3zpB0u4LwWTVJ4",
        "video_id": None,
        "playlist_id": "RDTMAK5uy_nilrsVWxrKskY0ZUpVZ3zpB0u4LwWTVJ4",
    },
    {
        # another suggested mix
        "url": "https://music.youtube.com/playlist?list=RDTMAK5uy_n_5IN6hzAOwdCnM8D8rzrs3vDl12UcZpA",
        "video_id": None,
        "playlist_id": "RDTMAK5uy_n_5IN6hzAOwdCnM8D8rzrs3vDl12UcZpA",
    },
]

YTM_VIDEO_IN_MIX_PLAYLISTS = [
    {
        # from create a mix
        "url": "https://music.youtube.com/watch?v=kPkT0jMjEu8&list=RDATmba11fjz9y3mcE",
        "video_id": "kPkT0jMjEu8",
        "playlist_id": "RDATmba11fjz9y3mcE",
    },
    {
        # from suggested mix
        "url": "https://music.youtube.com/watch?v=mewl5TnLRRE&list=RDTMAK5uy_nilrsVWxrKskY0ZUpVZ3zpB0u4LwWTVJ4",
        "video_id": "mewl5TnLRRE",
        "playlist_id": "RDTMAK5uy_nilrsVWxrKskY0ZUpVZ3zpB0u4LwWTVJ4",
    },
    {
        # another from suggested mix
        "url": "https://music.youtube.com/watch?v=pWO718iy5mY&list=RDTMAK5uy_n_5IN6hzAOwdCnM8D8rzrs3vDl12UcZpA",
        "video_id": "pWO718iy5mY",
        "playlist_id": "RDTMAK5uy_n_5IN6hzAOwdCnM8D8rzrs3vDl12UcZpA",
    },
]

EDGE_URLS = [
    {
        # blank url
        "url": "",
        "video_id": None,
        "playlist_id": None,
    },
    {
        # no video_id, yt_dlp.utils.DownloadError: ERROR: Unsupported URL: https://music.youtube.com/watch?v=
        "url": "https://music.youtube.com/watch?v=",
        "video_id": None,
        "playlist_id": None,
    },
    {
        # no playlist_id, yt_dlp.utils.DownloadError: ERROR: [generic] Unable to download webpage: HTTP Error 404: Not Found (caused by <HTTPError 404: Not Found>)
        "url": "https://www.youtube.com/playlist?list=",
        "video_id": None,
        "playlist_id": None,
    },
    {
        # no video_id and playlist_id
        "url": "https://www.youtube.com/watch?v=&list=&index=2&t=36s",
        "video_id": None,
        "playlist_id": None,
    },
    {
        # no video_id but playlist_id, yt_dlp.utils.DownloadError: ERROR: Unsupported URL: https://music.youtube.com/playlist?list=
        "url": "https://www.youtube.com/watch?v=&list=PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT&index=2&t=36s",
        "video_id": None,
        "playlist_id": "PLQSoWXSpjA39U94TANpW67fxfYhm5CFFT",
    },
    {
        # no playlist_id but video_id, works properly to get video
        "url": "https://www.youtube.com/watch?v=0PAEqgfAts4&list=&index=2&t=36s",
        "video_id": "0PAEqgfAts4",
        "playlist_id": None,
    },
    {
        # all 0 video_id, yt: not found (for any length of 0), yt_dlp.utils.DownloadError: ERROR: [youtube] 00000000000: Video unavailable
        "url": "https://www.youtube.com/watch?v=00000000000",
        "video_id": "00000000000",
        "playlist_id": None,
    },
    {
        # invalid video_id length < 11, yt_dlp.utils.DownloadError: ERROR: [youtube:truncated_id] 0PAEqgfAts: Incomplete YouTube ID 0PAEqgfAts. URL https://www.youtube.com/watch?v=0PAEqgfAts looks truncated.
        "url": "https://www.youtube.com/watch?v=0PAEqgfAts",
        "video_id": "0PAEqgfAts",
        "playlist_id": None,
    },
    {
        # invalid video_id length > 11, works fine to get the video
        "url": "https://www.youtube.com/watch?v=0PAEqgfAts46969",
        "video_id": "0PAEqgfAts46969",
        "playlist_id": None,
    },
    {
        # yt: all 0 id playlist leads back to home page, yt_dlp.utils.DownloadError: ERROR: [youtube:tab] 0000000000000000000000000000000000: Unable to download API page: HTTP Error 400: Bad Request (caused by <HTTPError 400: Bad Request>)
        "url": "https://www.youtube.com/playlist?list=0000000000000000000000000000000000",
        "video_id": None,
        "playlist_id": "0000000000000000000000000000000000",
    },
    {
        # valid private playlist, yt_dlp.utils.DownloadError: ERROR: [youtube:tab] PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC: YouTube said: The playlist does not exist.
        "url": "https://www.youtube.com/playlist?list=PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC",
        "video_id": None,
        "playlist_id": "PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC",
    },
    {
        # public video in valid private playlist, ytdlp no error but no info
        "url": "https://www.youtube.com/watch?v=S5jROs3A6F8&list=PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC&index=2",
        "video_id": "S5jROs3A6F8",
        "playlist_id": "PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC",
    },
    {
        # valid private video, yt_dlp.utils.DownloadError: ERROR: [youtube] HkeLXf7sYGM: Private video. Sign in if you've been granted access to this video. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies
        "url": "https://www.youtube.com/watch?v=HkeLXf7sYGM",
        "video_id": "HkeLXf7sYGM",
        "playlist_id": None,
    },
    {
        # valid private video in private playlist, ytdlp no error but no info
        "url": "https://www.youtube.com/watch?v=HkeLXf7sYGM&list=PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC&index=6",
        "video_id": "HkeLXf7sYGM",
        "playlist_id": "PLlAZKtV48pBbC4nlImTJtM7TVGl0aEolC",
    },
]
