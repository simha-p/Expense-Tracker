import React from 'react';

function Alert({ type, message, onClose }) {
  return (
    <div className={`alert alert-${type}`}>
      <span>{message}</span>
      <button
        className="alert-close"
        onClick={onClose}
        aria-label="Close alert"
      >
        ×
      </button>
    </div>
  );
}

export default Alert;
