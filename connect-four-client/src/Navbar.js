import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>Connect Four Online</h1>
      <div className="links">
        <Link to="/">Home</Link>
        <Link to="/signup">Signup/Login</Link>
      </div>
    </nav>
  );
}
 
export default Navbar;