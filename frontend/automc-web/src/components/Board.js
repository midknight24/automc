import { Col, Row } from 'antd'
import { QuizForm } from './Form.js'
import { Result } from './Result.js'

export function Board() {
  return (
    <>
      <Row>
        <Col span={12}>
          <QuizForm></QuizForm>
        </Col>
        <Col span={12}>
          <Result></Result>
        </Col>
      </Row>
    </>
  )
}