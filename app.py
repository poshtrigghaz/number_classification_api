from flask import Flask, request, jsonify
import math
import requests

app = Flask(__name__)

def is_armstrong(number):
    digits = [int(d) for d in str(abs(int(number)))]
    return sum(d ** len(digits) for d in digits) == number

def is_perfect(number):
    return sum(i for i in range(1, int(number)) if number % i == 0) == number

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    try:
        parsed_number = float(number)
        is_int = parsed_number.is_integer()
        parsed_number = int(parsed_number) if is_int else parsed_number

        digit_sum = sum(int(d) for d in str(abs(int(parsed_number))))
        properties = []
        if is_armstrong(parsed_number) and is_int:
            properties.append("armstrong")
        properties.append("odd" if parsed_number % 2 != 0 else "even" if is_int else "n/a")

        is_perfect_number = is_perfect(parsed_number) if is_int else False
        is_prime = (
            all(parsed_number % i != 0 for i in range(2, int(math.sqrt(parsed_number)) + 1)) and parsed_number > 1
            if is_int else False
        )

        try:
            response = requests.get(f"http://numbersapi.com/{parsed_number}/math", timeout=5)
            fun_fact = response.text if response.status_code == 200 else "Fun fact not found."
        except:
            fun_fact = "Could not fetch fun fact."

        return jsonify({
            "number": parsed_number,
            "is_prime": is_prime,
            "is_perfect": is_perfect_number,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }), 200

    except ValueError:
        return jsonify({"number": number, "error": True}), 400

if __name__ == '__main__':
    app.run(debug=True)
