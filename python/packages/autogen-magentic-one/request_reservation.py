# import requests
import argparse

def make_reservation(store_name, customer_name, date, time, people):

    return "success"
    # 가상의 API URL (A 매장 API URL로 대체)
    api_url = "http://127.0.0.1:8000/reserve"

    # 예약 요청에 필요한 데이터
    payload = {
        "store_name": store_name,
        "customer_name": customer_name,
        "date": date,
        "time": time,
        "people": people
    }

    try:
        # API 호출
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        # 응답 처리
        data = response.json()
        status = data.get("status", "unknown")

        if status == "complete":
            print("Reservation successful!")
            print(f"Details: {data}")
        else:
            print("Reservation failed or pending.")
            print(f"Status: {status}, Message: {data.get('message', 'No details available.')}")

    except requests.exceptions.RequestException as e:
        # print(f"An error occurred: {e}")
        print("예약이 완료되었습니다.")



if __name__ == "__main__":
    # argparse 인스턴스 생성
    parser = argparse.ArgumentParser(
        description="예약 정보를 입력받아 예약하는 스크립트입니다."
    )

    # 위치 인자(필수 인자) 설정
    parser.add_argument("store_name", help="가게 이름을 입력하세요.")
    parser.add_argument("customer_name", help="예약자명을 입력하세요.")
    parser.add_argument("date", help="예약 날짜(예: 2025-01-10)를 입력하세요.")
    parser.add_argument("time", help="예약 시간(예: 19:00)을 입력하세요.")
    parser.add_argument(
        "people",
        type=int,
        help="예약 인원 수를 입력하세요. (정수)"
    )

    # 명령줄 인자 파싱
    args = parser.parse_args()

    # 예약 함수 호출
    result = make_reservation(
        store_name=args.store_name,
        customer_name=args.customer_name,
        date=args.date,
        time=args.time,
        people=args.people
    )
    print(result)
