import { Input } from 'antd'

export function Result({data}) {
    return (
    <>
        <Input.TextArea value={data} autoSize={{ minRows: 20, maxRows: 20 }} />
    </>
    )
}