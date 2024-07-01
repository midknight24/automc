import { Form, Input, Select, message, Button, Space, Divider  } from 'antd'
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
  }, [form,form.getFieldValue('backendUrl')])


  return (
    <>
    <Space.Compact block style={{marginBottom: '10px'}}>
      <Input placeholder="backend addr"/>
      <Button type="primary">Submit</Button>
    </Space.Compact>
    <Form
      form={form}
      onFinish
    >
      <Form.Item name="llm" label="llm">
        <Select options={options}></Select>
      </Form.Item>
    </Form>
    </>
  )
}
