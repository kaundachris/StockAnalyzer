from GetData import GetSpecificData


def main():
    try:
        company_info = GetSpecificData('TSLA')
        return company_info.write_specific_data()
    except NameError as message:
        return message


if __name__ == '__main__':
    print(main())
