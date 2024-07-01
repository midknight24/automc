import { Form, Input, Select, message } from 'antd'
import { useState, useEffect } from 'react'
import { getLLM } from '../backend/api'

export function QuizForm() {
  const [form] = Form.useForm()
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(()=>{
    try {
      const data = getLLM()
      console.log(data)
      setOptions(data)
    } catch(err) {
      message.error(err)
    }
  }, [])


  return (
    <Form
      form={form}
      onFinish
    >
      <Form.Item name="backendUrl" label="url">
        <Input></Input>
      </Form.Item>
      <Form.Item name="llm" label="llm">
        <Select options={options}></Select>
      </Form.Item>
    </Form>
  )
}
