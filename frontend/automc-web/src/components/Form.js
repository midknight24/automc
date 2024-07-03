import { Form, Input, Select, Button, Space, Switch  } from 'antd'
import { useEffect, useState } from 'react'
import { getLLM, UpdateURL, genQuiz } from '../backend/api'

export function QuizForm({onSubmitReturn}) {
  const [form] = Form.useForm()
  const [url, setUrl] = useState('http://localhost:8000');
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setFormSubmitting] = useState(false);
  
  const UpdateSelect = async () => {
    console.log("updating api addr: ", url)
    UpdateURL(url)
    setLoading(true)
    const data = await getLLM()
    console.log(data)
    setOptions(data.map((el)=>{
      return {value: el.id, label: el.model_vendor}
    }))
    setLoading(false)
  }

  const SubmitForm = async (values) => {
    console.log(values)
    values.content = JSON.stringify(values.content)
    setFormSubmitting(true)
    const data = await genQuiz(values)
    console.log(data)
    onSubmitReturn(data)
    setFormSubmitting(false)
  }

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  useEffect(()=>{UpdateSelect()}, [])

  return (
    <>
    <Space.Compact block style={{marginBottom: '20px'}}>
      <Input value={url} placeholder="backend addr" onChange={handleInputChange}/>
      <Button type="primary" onClick={UpdateSelect} loading={loading}>Submit</Button>
    </Space.Compact>
    <Form
      form={form}
      onFinish={SubmitForm}
    >
      <Form.Item name="llm_id" label="llm">
        <Select options={options}></Select>
      </Form.Item>
      <Space>
      <Form.Item name="pick_best" label="pick_best">
        <Switch/>
      </Form.Item>
      <Form.Item name="oneshot" label="oneshot">
        <Switch/>
      </Form.Item>
      </Space>
      <Form.Item name="content" label="content">
        <Input.TextArea autoSize={{ minRows: 7, maxRows: 20 }} />
      </Form.Item>
      <Button block type="primary" htmlType="submit" loading={submitting}>Submit</Button>
    </Form>
    </>
  )
}
