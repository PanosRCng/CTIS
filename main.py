import argparse




def main():

    parser = argparse.ArgumentParser("main.py", description='Context-Aware Term Informativeness System')
    subparsers = parser.add_subparsers(help='operations', dest='operation')

    start_server_parser = subparsers.add_parser('start', help='starts the server')

    bootstrap_knowledge_base_parser = subparsers.add_parser('bootstrap_knowledge_base', help='bootstraps the knowledge base using an offline wikipedia dump')
    bootstrap_knowledge_base_parser.add_argument('dump_directory', metavar='dump_directory', type=str, help='the offline wikipedia dump specified by its filesystem path')

    clear_knowledge_base_parser = subparsers.add_parser('clear_knowledge_base', help='removes all entries from the knowledge base')


    args = vars(parser.parse_args())

    if args['operation'] == 'start':
        import cti
        cti.start_server()

    if args['operation'] == 'bootstrap_knowledge_base':
        import cti
        return cti.bootstrap_knowledge_base(args['dump_directory'])

    if args['operation'] == 'clear_knowledge_base':
        import cti
        cti.clear_knowledge_base()





if __name__ == '__main__':
    main()


