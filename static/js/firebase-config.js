// Import Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, sendPasswordResetEmail, signInWithPopup, GoogleAuthProvider, signOut } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

// Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyCoL7AS8Og8uS59cVT_sxYOiY7hHn44wXE",
  authDomain: "vigneshaniruth-ba64b.firebaseapp.com",
  projectId: "vigneshaniruth-ba64b",
  storageBucket: "vigneshaniruth-ba64b.firebasestorage.app",
  messagingSenderId: "173942599225",
  appId: "1:173942599225:web:5ad050a8592957bec527e8",
  measurementId: "G-ZE8DYRXNGF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// ✅ Google Login
window.googleLogin = function () {
    signInWithPopup(auth, provider)
        .then((result) => {
            const user = result.user;
            alert("Welcome " + user.displayName);
            window.location.href = "/home";
        })
        .catch((error) => {
            alert(error.message);
        });
}

// ✅ Email & Password Login
window.emailLogin = function () {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Login Successful!");
            window.location.href = "/home";
        })
        .catch((error) => {
            alert(error.message);
        });
}

// ✅ Register
window.register = function () {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Registration Successful!");
            window.location.href = "/home";
        })
        .catch((error) => {
            alert(error.message);
        });
}

// ✅ Forgot Password
window.forgotPassword = function () {
    const email = document.getElementById('login-email').value;
    if (!email) {
        alert("Please enter your email to reset password.");
        return;
    }
    sendPasswordResetEmail(auth, email)
        .then(() => {
            alert("Password reset link sent to email.");
        })
        .catch((error) => {
            alert(error.message);
        });
}

// ✅ Logout
window.logout = function () {
    signOut(auth).then(() => {
        alert("Logged Out");
        window.location.href = "/";
    });
}
