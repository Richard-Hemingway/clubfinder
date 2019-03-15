# clubfinder

clubfinder is an SQLite database of Rifle Shooting Clubs in the United Kingdom.

It currently covers more than 500 clubs. The Channel Islands, Isle of Man, Northern Ireland, Wales, and Scotland are broadly complete whilst England is good up to counties starting with "O".

## Why?

There are a million and one club-finders on the web in various states of decay, each having set out to be more accurate or user-friendly than the last and then abandoned. It is quite hard to get stale information updated or amended in those abandoned datasets.

Unfortunately, each time someone sets out to build one that is up-to-date, they have to start from scratch, inevitably piling data into their own private silo. This repo contains an SQLite database with a basic listing of clubs, along with their County/Country and basic data like web address, a rough idea of their discipline coverage and whether or not they are a University Club.

This dataset contains no GDPR-Regulated data. It also contains no precise location data such as physical addresses, postcodes or coordinates.

It is my hope that in future, organisations and associations can use this data source in their club finders and receive updates by simply copying in the latest version of the database. None of this should be necessary of course, since our NGBs should have comprehensive and full-featured club-finders exported direct from their databases of Affiliated Clubs. However, this is apparently not the case, so here's a free, open alternative that users can build upon.

## Data Sources

The first pass consists mostly of smallbore clubs turned up web.archive.org copies of the NSRA's old ClubFinder plus a bunch of Google Searches (since the Internet Archive apparently did not archive all of it). It does however include fullbore clubs as they have turned up, and recognises multi-disciplinary clubs which affiliate to both NSRA *and* NRA.

## Contributing

You are encouraged to submit Pull Requests with updated data. It should be preferable to push changes to the master file as a single, publicly-maintained source of truth rather than editing your own private copy/fork and having to rebase your modified file with an updated master file.

Pull requests will only be accepted for the actual clubfinder.sqlite database. Any subsidiary files or reports (e.g. extracts in csv format) that I may get around to outputting for people's convenience are/will be generated from that master file, meaning that each time the SQLite file is updated, those reports will be overwritten so please do not invest time or effort in updating them! They are intended for Read-Only consumption. If you are not comfortable updating the SQLite database yourself and submitting a Pull Request, you can log missing clubs or incorrect data as bugs or comments.

## License

The dataset is licensed under the CC-BY-SA-4.0 license which allows extremely broad reuse (including commercial) provided that you acknowledge the project. See [LICENSE](LICENSE.md) file for full details.