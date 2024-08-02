import one_file
import all_files

print("\n[Select]")
print("하나의 파일(사진)에 대해 실행 : 0")
print("폴더 내의 모든 파일에 대해 실행 : 1\n")

select = int(input("0 또는 1을 입력해주세요 : "))

if(select == 0):
    one_file.start()
elif(select == 1):
    all_files.start()
else:
    print("잘못된 수입니다 재실행 해주세요.")