from functions.get_file_content import get_file_content

def main() -> None:
    result = get_file_content("calculator", "lorem.txt")
    if 'Error' not in result[:6]:
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")
    else:
        print(result)
    result = get_file_content("calculator", "main.py")
    if 'Error' not in result[:6]:  
        print(f"main.py length: {len(result)}")
        print(f"main.py truncated: {'truncated' in result}")
        print(result)
    else:
        print(result)
    result = get_file_content('calculator', 'pkg/calculator.py')
    if 'Error' not in result[:6]:  
        print(f"pkg/calculator.py length: {len(result)}")
        print(f"pkg/calculator.py truncated: {'truncated' in result}")
        print(result)
    else:
        print(result)
    result = get_file_content('calculator', '/bin/cat')
    if 'Error' not in result[:6]:
        print(f"/bin/cat length: {len(result)}")
        print(f"/bin/cat truncated: {'truncated' in result}")
        print(result)
    else:
        print(result)
    result = get_file_content('calculator', 'pkg/does_not_exist.py')
    if 'Error' not in result[:6]:
        print(f"pkg/does_not_exist.py length: {len(result)}")
        print(f"pkg/does_not_exist.py truncated: {'truncated' in result}")
        print(result)
    else:
        print(result)

if __name__ == "__main__":
    main()