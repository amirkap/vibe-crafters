import json

mock_openai_response = '''{
    "seed_artists": "Bee Gees,KC and The Sunshine Band",
    "seed_tracks": "Stayin' Alive - Bee Gees,That's the Way (I Like It) - KC and The Sunshine Band",
    "target_valence": 0.8,
    "min_valence": 0.7,
    "max_valence": 1.0,
    "target_danceability": 0.8,
    "min_danceability": 0.7,
    "max_danceability": 1.0,
    "target_energy": 0.8,
    "min_energy": 0.7,
    "max_energy": 1.0
}'''
mock_find_spotify_seeds_response = {"seed_tracks": "7g4I3DeFlZLeqMjw0ONBqs,7fu3Tv5rcoGD1PZV7s57WW",
                                    "seed_artists": "6PpGPIrFf3LM7Q77eR4Bts,0Xf8oDAJYd2D0k3NLI19OV"}
mock_find_min_tracks_response = ['2QaTacWkV0bC68QYNCI3k6', '1spr3ff7dxssldzMZmoITf', '5AIKhsRdThwwXMRoHpYPRt', '5FMlvzPFVvHTvz8V2bwvpp', '6k8Ckm7e5IRwWSIeAduP4b', '79OzqW7Dril4hY5gu1XA8z', '3HsBtrErYQjxf4Pv2p05Oy', '3xBGofZKEsxXHJu7ACzrao', '55cMXcQ8FltQchOV84EhyX', '3pNFl9UJAMlFXCGnkBZoDz']
mock_get_recommendations_response = json.loads('''[
  {
    "album": {
      "album_type": "compilation",
      "total_tracks": 9,
      "available_markets": [
        "CA",
        "BR",
        "IT"
      ],
      "external_urls": {
        "spotify": "string"
      },
      "href": "string",
      "id": "2up3OPMp9Tb4dAKM2erWXQ",
      "images": [
        {
          "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
          "height": 300,
          "width": 300
        }
      ],
      "name": "string",
      "release_date": "1981-12",
      "release_date_precision": "year",
      "restrictions": {
        "reason": "market"
      },
      "type": "album",
      "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
      "artists": [
        {
          "external_urls": {
            "spotify": "string"
          },
          "href": "string",
          "id": "string",
          "name": "string",
          "type": "artist",
          "uri": "string"
        }
      ]
    },
    "artists": [
      {
        "external_urls": {
          "spotify": "string"
        },
        "followers": {
          "href": "string",
          "total": 0
        },
        "genres": [
          "Prog rock",
          "Grunge"
        ],
        "href": "string",
        "id": "string",
        "images": [
          {
            "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
            "height": 300,
            "width": 300
          }
        ],
        "name": "string",
        "popularity": 0,
        "type": "artist",
        "uri": "string"
      }
    ],
    "available_markets": [
      "string"
    ],
    "disc_number": 0,
    "duration_ms": 0,
    "explicit": false,
    "external_ids": {
      "isrc": "string",
      "ean": "string",
      "upc": "string"
    },
    "external_urls": {
      "spotify": "string"
    },
    "href": "string",
    "id": "string",
    "is_playable": false,
    "linked_from": {},
    "restrictions": {
      "reason": "string"
    },
    "name": "string",
    "popularity": 0,
    "preview_url": "string",
    "track_number": 0,
    "type": "track",
    "uri": "string",
    "is_local": false
  }
]''')
mock_search_item_response = {
    "playlists": {
        "href": "https://api.spotify.com/v1/search?query=80s+happy+disco&type=playlist&market=US&offset=0&limit=10",
        "items": [
            {
                "collaborative": False,
                "description": "80s Happy Dance music picked just for you",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/37i9dQZF1EIdGyqVN5c9uD"
                },
                "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIdGyqVN5c9uD",
                "id": "37i9dQZF1EIdGyqVN5c9uD",
                "images": [
                    {
                        "height": None,
                        "url": "https://seed-mix-image.spotifycdn.com/v6/img/desc/80s%20Happy%20Dance/en/large",
                        "width": None
                    }
                ],
                "name": "80s Happy Dance Mix",
                "owner": {
                    "display_name": "Spotify",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/spotify"
                    },
                    "href": "https://api.spotify.com/v1/users/spotify",
                    "id": "spotify",
                    "type": "user",
                    "uri": "spotify:user:spotify"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MTk4MDIsMDAwMDAwMDBiYzE2ZGNmMzVkOWQyYWFkYmJhMWI0NjM3NDE4NDdjMA==",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIdGyqVN5c9uD/tracks",
                    "total": 50
                },
                "type": "playlist",
                "uri": "spotify:playlist:37i9dQZF1EIdGyqVN5c9uD"
            },
            {
                "collaborative": False,
                "description": "",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/7G0m6ixIhnKSFvXvdrqEsd"
                },
                "href": "https://api.spotify.com/v1/playlists/7G0m6ixIhnKSFvXvdrqEsd",
                "id": "7G0m6ixIhnKSFvXvdrqEsd",
                "images": [
                    {
                        "height": 640,
                        "url": "https://mosaic.scdn.co/640/ab67616d0000b2735133753da25ff4ba01c07d41ab67616d0000b27353ab68a90f4d9eb5f8e1a6b6ab67616d0000b2735616da918044142aa2eedaa1ab67616d0000b273b0d9d06a4d9555946e0c83cb",
                        "width": 640
                    },
                    {
                        "height": 300,
                        "url": "https://mosaic.scdn.co/300/ab67616d0000b2735133753da25ff4ba01c07d41ab67616d0000b27353ab68a90f4d9eb5f8e1a6b6ab67616d0000b2735616da918044142aa2eedaa1ab67616d0000b273b0d9d06a4d9555946e0c83cb",
                        "width": 300
                    },
                    {
                        "height": 60,
                        "url": "https://mosaic.scdn.co/60/ab67616d0000b2735133753da25ff4ba01c07d41ab67616d0000b27353ab68a90f4d9eb5f8e1a6b6ab67616d0000b2735616da918044142aa2eedaa1ab67616d0000b273b0d9d06a4d9555946e0c83cb",
                        "width": 60
                    }
                ],
                "name": "80s High Energy Disco Mix",
                "owner": {
                    "display_name": "Stefan Ebner",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/1140713709"
                    },
                    "href": "https://api.spotify.com/v1/users/1140713709",
                    "id": "1140713709",
                    "type": "user",
                    "uri": "spotify:user:1140713709"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MzEsMWViNTM4ODA0NWJmZDQ0Y2E0ZjA0ZDFiNTNhNzQ5NmY4NGQ3OGRlNg==",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/7G0m6ixIhnKSFvXvdrqEsd/tracks",
                    "total": 29
                },
                "type": "playlist",
                "uri": "spotify:playlist:7G0m6ixIhnKSFvXvdrqEsd"
            },
            {
                "collaborative": False,
                "description": "Best Of Disco Funk 70s, 80s, 90s, 2000s, Disco Party... From Daddy Cool to Born To Be Alive... Le Freak to Barbie Girl... YMCA to Freed From Desire... September to Cold Heart...  <a href=\"https://open.spotify.com/playlist/6RGKHL5iSqwJ8xv1zDj228?si=01962e8db0144027\">Click Here for BEST OF 80's </a>",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/0aSvbpDVaEBTv9dPiXrndk"
                },
                "href": "https://api.spotify.com/v1/playlists/0aSvbpDVaEBTv9dPiXrndk",
                "id": "0aSvbpDVaEBTv9dPiXrndk",
                "images": [
                    {
                        "height": None,
                        "url": "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000bebb949b7d553c6a14d2245b4a4d",
                        "width": None
                    }
                ],
                "name": "Disco Hits 80 90",
                "owner": {
                    "display_name": "Mama Disco 💃",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/rajtens"
                    },
                    "href": "https://api.spotify.com/v1/users/rajtens",
                    "id": "rajtens",
                    "type": "user",
                    "uri": "spotify:user:rajtens"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MTY0NyxlNDE5NDRlNjUwMzU2ZTY1YmM2MmQ5MjY4Y2U4NTU4MGQwNmQ3YzUy",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/0aSvbpDVaEBTv9dPiXrndk/tracks",
                    "total": 249
                },
                "type": "playlist",
                "uri": "spotify:playlist:0aSvbpDVaEBTv9dPiXrndk"
            },
            {
                "collaborative": False,
                "description": "r&amp;b, soul, funk, disco, jazz, pop, rock...",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/4lwzrP49exhEmZ4xY47plW"
                },
                "href": "https://api.spotify.com/v1/playlists/4lwzrP49exhEmZ4xY47plW",
                "id": "4lwzrP49exhEmZ4xY47plW",
                "images": [
                    {
                        "height": None,
                        "url": "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000bebbe7bc843f05042cca612aa312",
                        "width": None
                    }
                ],
                "name": "Happy 70's & 80's",
                "owner": {
                    "display_name": "elenasudria",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/elenasudria"
                    },
                    "href": "https://api.spotify.com/v1/users/elenasudria",
                    "id": "elenasudria",
                    "type": "user",
                    "uri": "spotify:user:elenasudria"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "NDMzLGI1YzVkZTkzNDQyMWRjNmNhM2NiOWJjZTRhMWU3ZWRmMDViNmY1MGY=",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/4lwzrP49exhEmZ4xY47plW/tracks",
                    "total": 1491
                },
                "type": "playlist",
                "uri": "spotify:playlist:4lwzrP49exhEmZ4xY47plW"
            },
            {
                "collaborative": False,
                "description": "80s Disco music picked just for you",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/37i9dQZF1EIg7JAIS4phis"
                },
                "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIg7JAIS4phis",
                "id": "37i9dQZF1EIg7JAIS4phis",
                "images": [
                    {
                        "height": None,
                        "url": "https://seed-mix-image.spotifycdn.com/v6/img/desc/80s%20Disco/en/large",
                        "width": None
                    }
                ],
                "name": "80s Disco Mix",
                "owner": {
                    "display_name": "Spotify",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/spotify"
                    },
                    "href": "https://api.spotify.com/v1/users/spotify",
                    "id": "spotify",
                    "type": "user",
                    "uri": "spotify:user:spotify"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MTk4MDIsMDAwMDAwMDBkZGFiNzMxNGRkNWYxOTg1ODE4NDRiODU2Yzk3M2MxMw==",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIg7JAIS4phis/tracks",
                    "total": 50
                },
                "type": "playlist",
                "uri": "spotify:playlist:37i9dQZF1EIg7JAIS4phis"
            },
            {
                "collaborative": False,
                "description": "&quot;Dancing&#x27;s part of my soul. I enjoy it, it makes people happy, and it makes me happy.&quot; -John Travolta | Disco, funk, soul, 80s pop. Anything classic that makes you wanna dance.",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/5HE54Cos6zdGyQeJI8aROm"
                },
                "href": "https://api.spotify.com/v1/playlists/5HE54Cos6zdGyQeJI8aROm",
                "id": "5HE54Cos6zdGyQeJI8aROm",
                "images": [
                    {
                        "height": None,
                        "url": "https://image-cdn-fa.spotifycdn.com/image/ab67706c0000bebb2cf6d65a2ea6f14789a9a2aa",
                        "width": None
                    }
                ],
                "name": "Boogie Fever",
                "owner": {
                    "display_name": "david.s.byrd",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/david.s.byrd"
                    },
                    "href": "https://api.spotify.com/v1/users/david.s.byrd",
                    "id": "david.s.byrd",
                    "type": "user",
                    "uri": "spotify:user:david.s.byrd"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "OTkwLGE4YTA2YTdkNjk3NDAwOTg5ZmQyN2JlZWRlN2ExOWNjZThkZWQ0NWM=",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/5HE54Cos6zdGyQeJI8aROm/tracks",
                    "total": 425
                },
                "type": "playlist",
                "uri": "spotify:playlist:5HE54Cos6zdGyQeJI8aROm"
            },
            {
                "collaborative": False,
                "description": "Feel Good 80s music picked just for you",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/37i9dQZF1EIh6LymxfLIVE"
                },
                "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIh6LymxfLIVE",
                "id": "37i9dQZF1EIh6LymxfLIVE",
                "images": [
                    {
                        "height": None,
                        "url": "https://seed-mix-image.spotifycdn.com/v6/img/desc/Feel%20Good%2080s/en/large",
                        "width": None
                    }
                ],
                "name": "Feel Good 80s Mix",
                "owner": {
                    "display_name": "Spotify",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/spotify"
                    },
                    "href": "https://api.spotify.com/v1/users/spotify",
                    "id": "spotify",
                    "type": "user",
                    "uri": "spotify:user:spotify"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MTk4MDIsMDAwMDAwMDA0YmQxOGI2MzdmNDlhNGQ1NGFkYjdkMGRhMDE5ZWE1OA==",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/37i9dQZF1EIh6LymxfLIVE/tracks",
                    "total": 50
                },
                "type": "playlist",
                "uri": "spotify:playlist:37i9dQZF1EIh6LymxfLIVE"
            },
            {
                "collaborative": False,
                "description": "Happy pop songs from 60&#x27;s, 70&#x27;s, 80&#x27;s, and 90&#x27;s and early 2000&#x27;s. Featuring Motown, Disco, Boy Bands, Country, Rock and Pop Princess hits.  No explicit lyrics. Safe for work or classroom.   (For newer hits, see my other playlist &quot;Classroom Mix - Modern Hits.)",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/4li9f3dtFoRC6J4gIhKRqb"
                },
                "href": "https://api.spotify.com/v1/playlists/4li9f3dtFoRC6J4gIhKRqb",
                "id": "4li9f3dtFoRC6J4gIhKRqb",
                "images": [
                    {
                        "height": None,
                        "url": "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000bebbbfbb724037cfb29e041cfbb6",
                        "width": None
                    }
                ],
                "name": "Classroom Mix - Retro Hits",
                "owner": {
                    "display_name": "joyfulshepherd",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/joyfulshepherd"
                    },
                    "href": "https://api.spotify.com/v1/users/joyfulshepherd",
                    "id": "joyfulshepherd",
                    "type": "user",
                    "uri": "spotify:user:joyfulshepherd"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "NzEzLDExZTZjOTI4ZThhYjE3OGZjNmUwNzdlMDEzMWI4MTU3Y2ZlNjg2OTY=",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/4li9f3dtFoRC6J4gIhKRqb/tracks",
                    "total": 534
                },
                "type": "playlist",
                "uri": "spotify:playlist:4li9f3dtFoRC6J4gIhKRqb"
            },
            {
                "collaborative": False,
                "description": "Freaky 80s punk and pop, a smidgin of rock, some happy Stevie Wonder and Bob Marley,  lots of terrible&#x2F;great disco and an Al Green fade out.",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/00rj0z1T6gikPyUFIGirGl"
                },
                "href": "https://api.spotify.com/v1/playlists/00rj0z1T6gikPyUFIGirGl",
                "id": "00rj0z1T6gikPyUFIGirGl",
                "images": [
                    {
                        "height": 640,
                        "url": "https://mosaic.scdn.co/640/ab67616d0000b2731fc9fd5d701ee05cb39b7b19ab67616d0000b2734121faee8df82c526cbab2beab67616d0000b2736b18e58a06aac7763abe319aab67616d0000b273d52bfb90ee8dfeda8378b99b",
                        "width": 640
                    },
                    {
                        "height": 300,
                        "url": "https://mosaic.scdn.co/300/ab67616d0000b2731fc9fd5d701ee05cb39b7b19ab67616d0000b2734121faee8df82c526cbab2beab67616d0000b2736b18e58a06aac7763abe319aab67616d0000b273d52bfb90ee8dfeda8378b99b",
                        "width": 300
                    },
                    {
                        "height": 60,
                        "url": "https://mosaic.scdn.co/60/ab67616d0000b2731fc9fd5d701ee05cb39b7b19ab67616d0000b2734121faee8df82c526cbab2beab67616d0000b2736b18e58a06aac7763abe319aab67616d0000b273d52bfb90ee8dfeda8378b99b",
                        "width": 60
                    }
                ],
                "name": "Dance songs from the 70s and 80s",
                "owner": {
                    "display_name": "otcpsych",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/otcpsych"
                    },
                    "href": "https://api.spotify.com/v1/users/otcpsych",
                    "id": "otcpsych",
                    "type": "user",
                    "uri": "spotify:user:otcpsych"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "ODksMjU3YmRlNWI1MmZlNjFiNThjMTUwNmFhNmMxNGNkNTBkYmI0NDU5ZA==",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/00rj0z1T6gikPyUFIGirGl/tracks",
                    "total": 52
                },
                "type": "playlist",
                "uri": "spotify:playlist:00rj0z1T6gikPyUFIGirGl"
            },
            {
                "collaborative": False,
                "description": "70s, 80s, 90s, 00s, 10s, RnB, Rap, Pop, Rock, Disco, EDM | HAPPY VIBES - ENERGY BOOST - ROAD TRIP | ",
                "external_urls": {
                    "spotify": "https://open.spotify.com/playlist/3FeRLTZJxtHg4XcARtU8oa"
                },
                "href": "https://api.spotify.com/v1/playlists/3FeRLTZJxtHg4XcARtU8oa",
                "id": "3FeRLTZJxtHg4XcARtU8oa",
                "images": [
                    {
                        "height": None,
                        "url": "https://image-cdn-ak.spotifycdn.com/image/ab67706c0000bebb688da65c62a69891a95155b8",
                        "width": None
                    }
                ],
                "name": "Top Hits of All Time",
                "owner": {
                    "display_name": "MVD",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/martijnvd99"
                    },
                    "href": "https://api.spotify.com/v1/users/martijnvd99",
                    "id": "martijnvd99",
                    "type": "user",
                    "uri": "spotify:user:martijnvd99"
                },
                "primary_color": None,
                "public": None,
                "snapshot_id": "MTI0NSwwZDk2ZDdlNjYwMDljNmRjMzQ0ZDljNTg0NWVkOGRhNDBlMTI5NmU2",
                "tracks": {
                    "href": "https://api.spotify.com/v1/playlists/3FeRLTZJxtHg4XcARtU8oa/tracks",
                    "total": 855
                },
                "type": "playlist",
                "uri": "spotify:playlist:3FeRLTZJxtHg4XcARtU8oa"
            }
        ],
        "limit": 10,
        "next": "https://api.spotify.com/v1/search?query=80s+happy+disco&type=playlist&market=US&offset=10&limit=10",
        "offset": 0,
        "previous": None,
        "total": 235
    }
}
mock_get_playlist_songs_response = json.loads('''{
    "href": "https://api.spotify.com/v1/playlists/4lwzrP49exhEmZ4xY47plW/tracks?offset=0&limit=2",
    "items": [
        {
            "added_at": "2020-03-07T17:11:00Z",
            "added_by": {
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/elenasudria"
                },
                "href": "https://api.spotify.com/v1/users/elenasudria",
                "id": "elenasudria",
                "type": "user",
                "uri": "spotify:user:elenasudria"
            },
            "is_local": false,
            "primary_color": null,
            "track": {
                "preview_url": "https://p.scdn.co/mp3-preview/4a80cc8373c7b4b4663d330b30e97b24abc808e9?cid=6a25b877d99f40129d446e4c78efe5b9",
                "available_markets": [
                    "AR",
                    "AU",
                    "AT",
                    "BE",
                    "BO",
                    "BR",
                    "BG",
                    "CA",
                    "CL",
                    "CO",
                    "CR",
                    "CY",
                    "CZ",
                    "DK",
                    "DO",
                    "DE",
                    "EC",
                    "EE",
                    "SV",
                    "FI",
                    "FR",
                    "GR",
                    "GT",
                    "HN",
                    "HK",
                    "HU",
                    "IS",
                    "IE",
                    "IT",
                    "LV",
                    "LT",
                    "LU",
                    "MY",
                    "MT",
                    "MX",
                    "NL",
                    "NZ",
                    "NI",
                    "NO",
                    "PA",
                    "PY",
                    "PE",
                    "PH",
                    "PL",
                    "PT",
                    "SG",
                    "SK",
                    "ES",
                    "SE",
                    "CH",
                    "TW",
                    "TR",
                    "UY",
                    "US",
                    "GB",
                    "AD",
                    "LI",
                    "MC",
                    "ID",
                    "JP",
                    "TH",
                    "VN",
                    "RO",
                    "IL",
                    "ZA",
                    "SA",
                    "AE",
                    "BH",
                    "QA",
                    "OM",
                    "KW",
                    "EG",
                    "MA",
                    "DZ",
                    "TN",
                    "LB",
                    "JO",
                    "PS",
                    "IN",
                    "BY",
                    "KZ",
                    "MD",
                    "UA",
                    "AL",
                    "BA",
                    "HR",
                    "ME",
                    "MK",
                    "RS",
                    "SI",
                    "KR",
                    "BD",
                    "PK",
                    "LK",
                    "GH",
                    "KE",
                    "NG",
                    "TZ",
                    "UG",
                    "AG",
                    "AM",
                    "BS",
                    "BB",
                    "BZ",
                    "BT",
                    "BW",
                    "BF",
                    "CV",
                    "CW",
                    "DM",
                    "FJ",
                    "GM",
                    "GE",
                    "GD",
                    "GW",
                    "GY",
                    "HT",
                    "JM",
                    "KI",
                    "LS",
                    "LR",
                    "MW",
                    "MV",
                    "ML",
                    "MH",
                    "FM",
                    "NA",
                    "NR",
                    "NE",
                    "PW",
                    "PG",
                    "WS",
                    "SM",
                    "ST",
                    "SN",
                    "SC",
                    "SL",
                    "SB",
                    "KN",
                    "LC",
                    "VC",
                    "SR",
                    "TL",
                    "TO",
                    "TT",
                    "TV",
                    "VU",
                    "AZ",
                    "BN",
                    "BI",
                    "KH",
                    "CM",
                    "TD",
                    "KM",
                    "GQ",
                    "SZ",
                    "GA",
                    "GN",
                    "KG",
                    "LA",
                    "MO",
                    "MR",
                    "MN",
                    "NP",
                    "RW",
                    "TG",
                    "UZ",
                    "ZW",
                    "BJ",
                    "MG",
                    "MU",
                    "MZ",
                    "AO",
                    "CI",
                    "DJ",
                    "ZM",
                    "CD",
                    "CG",
                    "IQ",
                    "LY",
                    "TJ",
                    "VE",
                    "ET",
                    "XK"
                ],
                "explicit": false,
                "type": "track",
                "episode": false,
                "track": true,
                "album": {
                    "available_markets": [
                        "AR",
                        "AU",
                        "AT",
                        "BE",
                        "BO",
                        "BR",
                        "BG",
                        "CA",
                        "CL",
                        "CO",
                        "CR",
                        "CY",
                        "CZ",
                        "DK",
                        "DO",
                        "DE",
                        "EC",
                        "EE",
                        "SV",
                        "FI",
                        "FR",
                        "GR",
                        "GT",
                        "HN",
                        "HK",
                        "HU",
                        "IS",
                        "IE",
                        "IT",
                        "LV",
                        "LT",
                        "LU",
                        "MY",
                        "MT",
                        "MX",
                        "NL",
                        "NZ",
                        "NI",
                        "NO",
                        "PA",
                        "PY",
                        "PE",
                        "PH",
                        "PL",
                        "PT",
                        "SG",
                        "SK",
                        "ES",
                        "SE",
                        "CH",
                        "TW",
                        "TR",
                        "UY",
                        "US",
                        "GB",
                        "AD",
                        "LI",
                        "MC",
                        "ID",
                        "JP",
                        "TH",
                        "VN",
                        "RO",
                        "IL",
                        "ZA",
                        "SA",
                        "AE",
                        "BH",
                        "QA",
                        "OM",
                        "KW",
                        "EG",
                        "MA",
                        "DZ",
                        "TN",
                        "LB",
                        "JO",
                        "PS",
                        "IN",
                        "BY",
                        "KZ",
                        "MD",
                        "UA",
                        "AL",
                        "BA",
                        "HR",
                        "ME",
                        "MK",
                        "RS",
                        "SI",
                        "KR",
                        "BD",
                        "PK",
                        "LK",
                        "GH",
                        "KE",
                        "NG",
                        "TZ",
                        "UG",
                        "AG",
                        "AM",
                        "BS",
                        "BB",
                        "BZ",
                        "BT",
                        "BW",
                        "BF",
                        "CV",
                        "CW",
                        "DM",
                        "FJ",
                        "GM",
                        "GE",
                        "GD",
                        "GW",
                        "GY",
                        "HT",
                        "JM",
                        "KI",
                        "LS",
                        "LR",
                        "MW",
                        "MV",
                        "ML",
                        "MH",
                        "FM",
                        "NA",
                        "NR",
                        "NE",
                        "PW",
                        "PG",
                        "WS",
                        "SM",
                        "ST",
                        "SN",
                        "SC",
                        "SL",
                        "SB",
                        "KN",
                        "LC",
                        "VC",
                        "SR",
                        "TL",
                        "TO",
                        "TT",
                        "TV",
                        "VU",
                        "AZ",
                        "BN",
                        "BI",
                        "KH",
                        "CM",
                        "TD",
                        "KM",
                        "GQ",
                        "SZ",
                        "GA",
                        "GN",
                        "KG",
                        "LA",
                        "MO",
                        "MR",
                        "MN",
                        "NP",
                        "RW",
                        "TG",
                        "UZ",
                        "ZW",
                        "BJ",
                        "MG",
                        "MU",
                        "MZ",
                        "AO",
                        "CI",
                        "DJ",
                        "ZM",
                        "CD",
                        "CG",
                        "IQ",
                        "LY",
                        "TJ",
                        "VE",
                        "ET",
                        "XK"
                    ],
                    "type": "album",
                    "album_type": "compilation",
                    "href": "https://api.spotify.com/v1/albums/4MgtwNYjD89Oj2km6eFRYd",
                    "id": "4MgtwNYjD89Oj2km6eFRYd",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/ab67616d0000b2736e5689a9d09ac1fc2cba2ab0",
                            "width": 640
                        },
                        {
                            "height": 300,
                            "url": "https://i.scdn.co/image/ab67616d00001e026e5689a9d09ac1fc2cba2ab0",
                            "width": 300
                        },
                        {
                            "height": 64,
                            "url": "https://i.scdn.co/image/ab67616d000048516e5689a9d09ac1fc2cba2ab0",
                            "width": 64
                        }
                    ],
                    "name": "September",
                    "release_date": "2018-04-17",
                    "release_date_precision": "day",
                    "uri": "spotify:album:4MgtwNYjD89Oj2km6eFRYd",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/4QQgXkCYTt3BlENzhyNETg"
                            },
                            "href": "https://api.spotify.com/v1/artists/4QQgXkCYTt3BlENzhyNETg",
                            "id": "4QQgXkCYTt3BlENzhyNETg",
                            "name": "Earth, Wind & Fire",
                            "type": "artist",
                            "uri": "spotify:artist:4QQgXkCYTt3BlENzhyNETg"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/album/4MgtwNYjD89Oj2km6eFRYd"
                    },
                    "total_tracks": 15
                },
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/4QQgXkCYTt3BlENzhyNETg"
                        },
                        "href": "https://api.spotify.com/v1/artists/4QQgXkCYTt3BlENzhyNETg",
                        "id": "4QQgXkCYTt3BlENzhyNETg",
                        "name": "Earth, Wind & Fire",
                        "type": "artist",
                        "uri": "spotify:artist:4QQgXkCYTt3BlENzhyNETg"
                    }
                ],
                "disc_number": 1,
                "track_number": 1,
                "duration_ms": 215080,
                "external_ids": {
                    "isrc": "USSM17800845"
                },
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/7Cuk8jsPPoNYQWXK9XRFvG"
                },
                "href": "https://api.spotify.com/v1/tracks/7Cuk8jsPPoNYQWXK9XRFvG",
                "id": "7Cuk8jsPPoNYQWXK9XRFvG",
                "name": "September",
                "popularity": 66,
                "uri": "spotify:track:7Cuk8jsPPoNYQWXK9XRFvG",
                "is_local": false
            },
            "video_thumbnail": {
                "url": null
            }
        },
        {
            "added_at": "2020-03-07T18:24:03Z",
            "added_by": {
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/elenasudria"
                },
                "href": "https://api.spotify.com/v1/users/elenasudria",
                "id": "elenasudria",
                "type": "user",
                "uri": "spotify:user:elenasudria"
            },
            "is_local": false,
            "primary_color": null,
            "track": {
                "preview_url": "https://p.scdn.co/mp3-preview/06c36139896754af7269ca5540bcd522e598518a?cid=6a25b877d99f40129d446e4c78efe5b9",
                "available_markets": [
                    "AR",
                    "AU",
                    "AT",
                    "BE",
                    "BO",
                    "BR",
                    "BG",
                    "CA",
                    "CL",
                    "CO",
                    "CR",
                    "CY",
                    "CZ",
                    "DK",
                    "DO",
                    "DE",
                    "EC",
                    "EE",
                    "SV",
                    "FI",
                    "FR",
                    "GR",
                    "GT",
                    "HN",
                    "HK",
                    "HU",
                    "IS",
                    "IE",
                    "IT",
                    "LV",
                    "LT",
                    "LU",
                    "MY",
                    "MT",
                    "MX",
                    "NL",
                    "NZ",
                    "NI",
                    "NO",
                    "PA",
                    "PY",
                    "PE",
                    "PH",
                    "PL",
                    "PT",
                    "SG",
                    "SK",
                    "ES",
                    "SE",
                    "CH",
                    "TW",
                    "TR",
                    "UY",
                    "US",
                    "GB",
                    "AD",
                    "LI",
                    "MC",
                    "ID",
                    "JP",
                    "TH",
                    "VN",
                    "RO",
                    "IL",
                    "ZA",
                    "SA",
                    "AE",
                    "BH",
                    "QA",
                    "OM",
                    "KW",
                    "EG",
                    "MA",
                    "DZ",
                    "TN",
                    "LB",
                    "JO",
                    "PS",
                    "IN",
                    "BY",
                    "KZ",
                    "MD",
                    "UA",
                    "AL",
                    "BA",
                    "HR",
                    "ME",
                    "MK",
                    "RS",
                    "SI",
                    "KR",
                    "BD",
                    "PK",
                    "LK",
                    "GH",
                    "KE",
                    "NG",
                    "TZ",
                    "UG",
                    "AG",
                    "AM",
                    "BS",
                    "BB",
                    "BZ",
                    "BT",
                    "BW",
                    "BF",
                    "CV",
                    "CW",
                    "DM",
                    "FJ",
                    "GM",
                    "GE",
                    "GD",
                    "GW",
                    "GY",
                    "HT",
                    "JM",
                    "KI",
                    "LS",
                    "LR",
                    "MW",
                    "MV",
                    "ML",
                    "MH",
                    "FM",
                    "NA",
                    "NR",
                    "NE",
                    "PW",
                    "PG",
                    "WS",
                    "SM",
                    "ST",
                    "SN",
                    "SC",
                    "SL",
                    "SB",
                    "KN",
                    "LC",
                    "VC",
                    "SR",
                    "TL",
                    "TO",
                    "TT",
                    "TV",
                    "VU",
                    "AZ",
                    "BN",
                    "BI",
                    "KH",
                    "CM",
                    "TD",
                    "KM",
                    "GQ",
                    "SZ",
                    "GA",
                    "GN",
                    "KG",
                    "LA",
                    "MO",
                    "MR",
                    "MN",
                    "NP",
                    "RW",
                    "TG",
                    "UZ",
                    "ZW",
                    "BJ",
                    "MG",
                    "MU",
                    "MZ",
                    "AO",
                    "CI",
                    "DJ",
                    "ZM",
                    "CD",
                    "CG",
                    "IQ",
                    "LY",
                    "TJ",
                    "VE",
                    "ET",
                    "XK"
                ],
                "explicit": false,
                "type": "track",
                "episode": false,
                "track": true,
                "album": {
                    "available_markets": [
                        "AR",
                        "AU",
                        "AT",
                        "BE",
                        "BO",
                        "BR",
                        "BG",
                        "CA",
                        "CL",
                        "CO",
                        "CR",
                        "CY",
                        "CZ",
                        "DK",
                        "DO",
                        "DE",
                        "EC",
                        "EE",
                        "SV",
                        "FI",
                        "FR",
                        "GR",
                        "GT",
                        "HN",
                        "HK",
                        "HU",
                        "IS",
                        "IE",
                        "IT",
                        "LV",
                        "LT",
                        "LU",
                        "MY",
                        "MT",
                        "MX",
                        "NL",
                        "NZ",
                        "NI",
                        "NO",
                        "PA",
                        "PY",
                        "PE",
                        "PH",
                        "PL",
                        "PT",
                        "SG",
                        "SK",
                        "ES",
                        "SE",
                        "CH",
                        "TW",
                        "TR",
                        "UY",
                        "US",
                        "GB",
                        "AD",
                        "LI",
                        "MC",
                        "ID",
                        "JP",
                        "TH",
                        "VN",
                        "RO",
                        "IL",
                        "ZA",
                        "SA",
                        "AE",
                        "BH",
                        "QA",
                        "OM",
                        "KW",
                        "EG",
                        "MA",
                        "DZ",
                        "TN",
                        "LB",
                        "JO",
                        "PS",
                        "IN",
                        "BY",
                        "KZ",
                        "MD",
                        "UA",
                        "AL",
                        "BA",
                        "HR",
                        "ME",
                        "MK",
                        "RS",
                        "SI",
                        "KR",
                        "BD",
                        "PK",
                        "LK",
                        "GH",
                        "KE",
                        "NG",
                        "TZ",
                        "UG",
                        "AG",
                        "AM",
                        "BS",
                        "BB",
                        "BZ",
                        "BT",
                        "BW",
                        "BF",
                        "CV",
                        "CW",
                        "DM",
                        "FJ",
                        "GM",
                        "GE",
                        "GD",
                        "GW",
                        "GY",
                        "HT",
                        "JM",
                        "KI",
                        "LS",
                        "LR",
                        "MW",
                        "MV",
                        "ML",
                        "MH",
                        "FM",
                        "NA",
                        "NR",
                        "NE",
                        "PW",
                        "PG",
                        "WS",
                        "SM",
                        "ST",
                        "SN",
                        "SC",
                        "SL",
                        "SB",
                        "KN",
                        "LC",
                        "VC",
                        "SR",
                        "TL",
                        "TO",
                        "TT",
                        "TV",
                        "VU",
                        "AZ",
                        "BN",
                        "BI",
                        "KH",
                        "CM",
                        "TD",
                        "KM",
                        "GQ",
                        "SZ",
                        "GA",
                        "GN",
                        "KG",
                        "LA",
                        "MO",
                        "MR",
                        "MN",
                        "NP",
                        "RW",
                        "TG",
                        "UZ",
                        "ZW",
                        "BJ",
                        "MG",
                        "MU",
                        "MZ",
                        "AO",
                        "CI",
                        "DJ",
                        "ZM",
                        "CD",
                        "CG",
                        "IQ",
                        "LY",
                        "TJ",
                        "VE",
                        "ET",
                        "XK"
                    ],
                    "type": "album",
                    "album_type": "album",
                    "href": "https://api.spotify.com/v1/albums/4RLVTxnuVN5ZWZqBFnaaQt",
                    "id": "4RLVTxnuVN5ZWZqBFnaaQt",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/ab67616d0000b2735ccd022a69a4da9551efd988",
                            "width": 640
                        },
                        {
                            "height": 300,
                            "url": "https://i.scdn.co/image/ab67616d00001e025ccd022a69a4da9551efd988",
                            "width": 300
                        },
                        {
                            "height": 64,
                            "url": "https://i.scdn.co/image/ab67616d000048515ccd022a69a4da9551efd988",
                            "width": 64
                        }
                    ],
                    "name": "I Am",
                    "release_date": "1979-06",
                    "release_date_precision": "month",
                    "uri": "spotify:album:4RLVTxnuVN5ZWZqBFnaaQt",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/4QQgXkCYTt3BlENzhyNETg"
                            },
                            "href": "https://api.spotify.com/v1/artists/4QQgXkCYTt3BlENzhyNETg",
                            "id": "4QQgXkCYTt3BlENzhyNETg",
                            "name": "Earth, Wind & Fire",
                            "type": "artist",
                            "uri": "spotify:artist:4QQgXkCYTt3BlENzhyNETg"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/album/4RLVTxnuVN5ZWZqBFnaaQt"
                    },
                    "total_tracks": 9
                },
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/4QQgXkCYTt3BlENzhyNETg"
                        },
                        "href": "https://api.spotify.com/v1/artists/4QQgXkCYTt3BlENzhyNETg",
                        "id": "4QQgXkCYTt3BlENzhyNETg",
                        "name": "Earth, Wind & Fire",
                        "type": "artist",
                        "uri": "spotify:artist:4QQgXkCYTt3BlENzhyNETg"
                    },
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/64CuUOOirKmdAYLQSfaOyr"
                        },
                        "href": "https://api.spotify.com/v1/artists/64CuUOOirKmdAYLQSfaOyr",
                        "id": "64CuUOOirKmdAYLQSfaOyr",
                        "name": "The Emotions",
                        "type": "artist",
                        "uri": "spotify:artist:64CuUOOirKmdAYLQSfaOyr"
                    }
                ],
                "disc_number": 1,
                "track_number": 5,
                "duration_ms": 288293,
                "external_ids": {
                    "isrc": "USSM19922860"
                },
                "external_urls": {
                    "spotify": "https://open.spotify.com/track/6ztstiyZL6FXzh4aG46ZPD"
                },
                "href": "https://api.spotify.com/v1/tracks/6ztstiyZL6FXzh4aG46ZPD",
                "id": "6ztstiyZL6FXzh4aG46ZPD",
                "name": "Boogie Wonderland",
                "popularity": 77,
                "uri": "spotify:track:6ztstiyZL6FXzh4aG46ZPD",
                "is_local": false
            },
            "video_thumbnail": {
                "url": null
            }
        }
    ],
    "limit": 2,
    "next": "https://api.spotify.com/v1/playlists/4lwzrP49exhEmZ4xY47plW/tracks?offset=2&limit=2",
    "offset": 0,
    "previous": null,
    "total": 1491
}''')
