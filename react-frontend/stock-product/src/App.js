


import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './components/Home';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import CreateProduct from './components/CreateProduct';


import HomePage from './components/HomePage';
import './components/css/Navbar.css'; 

function App() {
  return (
    <Router>
      <div>
        <nav className="navbar">
          <Link to="/" className="nav-link">Logout</Link>
          <Link to="/products" className="nav-link">Products</Link>
          <Link to="/create_product" className="nav-link">Create Product</Link>
          
          <Link to="/homepage" className="nav-link">HomePage</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<ProductList />} />
         
          <Route path="/products/:productId" element={<ProductDetail />} /> 
          <Route path="/create_product" element={<CreateProduct />} />
          
          <Route path="/homepage" element={<HomePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
