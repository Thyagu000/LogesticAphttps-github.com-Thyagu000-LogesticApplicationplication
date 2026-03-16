import "./ContactSupport.css";
import { FaArrowLeft, FaQuestionCircle } from "react-icons/fa";
import { MdChat, MdEmail, MdPhone, MdMenuBook } from "react-icons/md";
import { FaHome } from "react-icons/fa";
import { FaTruck} from "react-icons/fa";
import { MdInventory } from "react-icons/md";
import { FaChartBar } from "react-icons/fa";

function ContactSupport() {
  return (
    <div className="support-page">

      {/* TOP BAR */}
      <div className="top-bar">
        <FaArrowLeft className="icon" />
        <h3>Contact Support</h3>
        <FaQuestionCircle className="icon" />
      </div>

      {/* HEADER */}
      <h2 className="title">How can we help?</h2>
      <p className="subtitle">
        Our logistics experts are standing by to assist with your shipments and delivery fleet.
      </p>

      {/* SUPPORT CARDS */}
      <div className="support-cards">

        <div className="card">
          <MdChat className="card-icon"/>
          <h3>Live Chat</h3>
          <p>Available 24/7</p>
        </div>

        <div className="card">
          <MdEmail className="card-icon"/>
          <h3>Email Support</h3>
          <p>2hr response time</p>
        </div>

        <div className="card">
          <MdPhone className="card-icon"/>
          <h3>Phone Call</h3>
          <p>Mon-Fri 9-6</p>
        </div>

        <div className="card">
          <MdMenuBook className="card-icon"/>
          <h3>Help Center</h3>
          <p>Self-service guides</p>
        </div>

      </div>

      {/* FORM */}
      <div className="form-section">

        <h3>Send us a message</h3>

        <label>Inquiry Type</label>
        <select>
          <option>General Shipping Inquiry</option>
          <option>Tracking Delay</option>
          <option>Payment Issue</option>
        </select>

        <label>Subject</label>
        <input type="text" placeholder="Tracking delay, etc." />

        <label>Message</label>
        <textarea placeholder="How can we help?" />

        <button className="submit-btn">Send Inquiry</button>

      </div>

      {/* BOTTOM NAV */}
      <div className="bottom-nav">
        <div><FaHome /><p>Home</p></div>
        <div><MdInventory /><p>Shipments</p></div>
        <div><FaTruck /><p>Fleet</p></div>
        <div><FaChartBar /><p>Analytics</p></div>
        <div className="active"><FaQuestionCircle /><p>Support</p></div>
      </div>

    </div>
  );
}

export default ContactSupport;