import { Form, Input, Select, Button, Space, Switch  } from 'antd'
import { useState } from 'react'
import { getLLM, UpdateURL } from '../backend/api'

export function QuizForm() {
  const [form] = Form.useForm()
  const [url, setUrl] = useState('');
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);

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

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  return (
    <>
    <Space.Compact block style={{marginBottom: '20px'}}>
      <Input value={url} placeholder="backend addr" onChange={handleInputChange}/>
      <Button type="primary" onClick={UpdateSelect} loading={loading}>Submit</Button>
    </Space.Compact>
    <Form
      form={form}
      onFinish
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
    </Form>
    <Button block type="primary">Submit</Button>
    </>
  )
}
