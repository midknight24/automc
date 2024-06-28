import logo from './logo.svg';
import './App.css';
import { Layout, theme } from 'antd';

const { Header, Content, Footer } = Layout;

function App() {

  const {
    token: { colorBgContainer, borderRadiusLG, colorTextBase },
  } = theme.useToken();


  return (
    <div className="App">
      <Layout>
        <Header style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{
            color: 'white',
            fontWeight: 'bold'
          }}>AUTOMC</div>
        </Header>
        <Content style={{ padding: '12px 48px' }} >
          <div
            style={{
              background: colorBgContainer,
              minHeight: 480,
              padding: 24,
              borderRadius: borderRadiusLG,
            }}
          >
            Content
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          Ant Design ©{new Date().getFullYear()} Created by Ant UED
        </Footer>
      </Layout>
    </div>
  );
}

export default App;
