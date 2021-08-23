twitter_oembed_url = "https://publish.twitter.com/oembed?url="


def compare_strs(s1, s2):
    def NFD(s):
        return unicodedata.normalize("NFD", s)

    return NFD(s1) in NFD(s2)


def find_matching_locations(text, location_list):
    matching_locations = []
    for loc in location_list:
        if compare_strs(loc.name.casefold(), text.casefold()):
            matching_locations.append(loc)
        else:
            for other_name in loc.alt_names.split(","):
                if compare_strs(other_name.casefold(), text.casefold()):
                    matching_locations.append(loc)
                    break

    # Return the fist match | TODO: Pick one of the locations better
    if len(matching_locations) >= 1:
        return matching_locations[0]
    else:
        return None


def identify_city(tweet_text):
    # Get all locations from database
    locations = Location.objects.filter(loc_type="City")
    # Check which known city is in the tweet
    return find_matching_locations(tweet_text, locations)


def identify_specific_location(tweet_text):
    # Get all locations from database
    locations = Location.objects.filter(~Q(loc_type="City"))
    # Check which known locations are in the tweet
    return find_matching_locations(tweet_text, locations)


def process_tweet(pub_link, pub_datetime):
    r = requests.get(twitter_oembed_url + pub_link)
    success = False
    if r.status_code == 200:
        data = r.json()
        embed_code = data["html"].replace(
            '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>',
            "",
        )
        # Add author if not already in list
        author, _ = Author.objects.get_or_create(
            name=data["author_name"], profile_link=data["author_url"]
        )
        city = identify_city(embed_code)
        location = identify_specific_location(embed_code)

        if city is None and location is None:
            longitude, latitude = None, None
            msg = "Unable to extract a location from this tweet. It is saved for manual review."
            require_review = True
        else:
            if location is not None:  # Use the specific location for long and lat
                longitude = location.longitude
                latitude = location.latitude
            else:
                longitude = city.longitude
                latitude = city.latitude
            msg = "Tweet added successfully"
            require_review = False

        try:
            rep = Report.objects.create(
                author=author,
                publication_time=pub_datetime + datetime.timedelta(hours=4),
                pub_link=pub_link,
                location=city,
                longitude=longitude,
                latitude=latitude,
                report_type="Help Needed",
                report_subtype="General",
                title=None,
                description=None,
                require_review=require_review,
                embed_code=embed_code,
            )
            success = True
        except IntegrityError:
            msg = "Tweet has already been added. Please add a new one."
            success = False

    else:
        msg = "Unable to retrieve this tweet. Please try again later."
    return msg, success
