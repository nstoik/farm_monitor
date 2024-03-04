const mockAuthLogin = {
  accessToken:
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzA4MzE0NzI0LCJqdGkiOiI5N2Q5ZmNhMi02YTE2LTQ1YjAtODkzOC1lZDViMDhmMjBlNjAiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE3MDgzMTQ3MjQsImNzcmYiOiIyNTAzNmMwNy0xMzdjLTQ3M2QtOGUwZi1iZTAyOTJkZjE5YTIiLCJleHAiOjE3MDgzMTU2MjR9.LqbMLaAZQh9tKzNkZwrr08iBYj2fmCUMUBKoYSfQsag',
  refreshToken:
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODMxNDcyNCwianRpIjoiMzA4MjE2ZDAtOTg5Ny00OWNkLWFkZjMtOWI2NTY2NzFlZjA1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjEsIm5iZiI6MTcwODMxNDcyNCwiY3NyZiI6IjBkYmFhZjNlLWY0MTItNDY2NS05Yjg3LTFjZWNhZDA1N2JjOSIsImV4cCI6MTcxMDkwNjcyNH0.kzGmJRHwJxFbL_r-X5hWYL3kWmajeEd7DJN35Tf6BE8'
}

const mockAuthRefresh = {
  accessToken:
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODMxODU5MSwianRpIjoiMDNkNWM4OWItZGRlZS00ZGExLTgwYmItYTk5YTFmNTRhMzlhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzA4MzE4NTkxLCJjc3JmIjoiMWUyYzhjMjEtNjI4MC00NDM5LTk0OGQtYjU2ZGFkMTNmOWIzIiwiZXhwIjoxNzA4MzE5NDkxfQ.Ln7rioORDscxxkrERnADYf4Pg9Unug_FnvZCnrxmBiE'
}

const mockAuthLoginSuccessResponse = {
  data: mockAuthLogin,
  status: 200,
  statusText: 'OK',
  headers: {},
  config: {},
  request: {}
}

const mockAuthRefreshSuccessResponse = {
  data: mockAuthRefresh,
  status: 200,
  statusText: 'OK',
  headers: {},
  config: {},
  request: {}
}

export { mockAuthLoginSuccessResponse, mockAuthRefreshSuccessResponse, mockAuthLogin }
