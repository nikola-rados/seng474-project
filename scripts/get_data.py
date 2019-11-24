from modules.collect import collect_data
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', '-k', help='API key', required=True)
    parser.add_argument('--match-id', '-m', type=int,
                        help='Starting match ID for lookup cycle',
                        required=True)
    parser.add_argument('--num-matches', '-n', default=5000, type=int,
                        help='Number of matches to collect')
    parser.add_argument('--outfile', '-o', default='match_data.json',
                        help='Data output file')
    args = parser.parse_args()

    # Default settings when run were:
    #   match_id = 5000012926
    #   loops = 5000
    collect_data(args.key, args.outfile, args.match_id, args.num_matches)
