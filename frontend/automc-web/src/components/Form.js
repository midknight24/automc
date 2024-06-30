import { Form, Input } from 'antd'

export function QuizForm() {
  const [form] = Form.useForm()
  return (
    <Form
      form={form}
      onFinish
    >
      <Form.Item name="backendUrl" label="url">
        <Input></Input>
      </Form.Item>W
    </Form>
  )
}
