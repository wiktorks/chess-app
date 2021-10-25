import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Link } from "react-router-dom";
// import Button from "react-bootstrap/Button"
import { useContext } from "react";
import { AuthContext } from "../../store/auth-context";

export const Navigation = () => {
  const authCtx = useContext(AuthContext);
  const isLoggedIn = authCtx.isLoggedIn;

  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="#home">ChessApp</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="ms-auto">
            {!isLoggedIn ? (
              <>
                <Link to="/auth">Login</Link>
                <Nav.Link eventKey={2} href="#memes">
                  Register
                </Nav.Link>
              </>
            ) : (
              <>
                <Link to="/profile">Profile</Link>
                <Nav.Link>Logout</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
