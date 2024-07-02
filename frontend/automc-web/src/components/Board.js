import { Col, Row } from 'antd'
import { QuizForm } from './Form.js'
import { Result } from './Result.js'
import { useState } from 'react'

export function Board() {
  const [result, setResult] = useState("");

  const handleQuizSubmit = (data) => {
    setResult(data);
  };

  return (
    <>
      <Row gutter={14}>
        <Col span={12}>
          <QuizForm onSubmitReturn={handleQuizSubmit}></QuizForm>
        </Col>
        <Col span={12}>
          <Result data={result}></Result>
        </Col>
      </Row>
    </>
  )
}