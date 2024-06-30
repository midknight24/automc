import axios from 'axios';

export const genQuiz = async (url, data) => {
    try {
        const resposne = await axios.post(url, data)
        return resposne.data
    } catch(error) {
        throw new Error()
    }
}