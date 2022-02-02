import "./App.css";
import {
  TextField,
  FormControl,
  InputLabel,
  NativeSelect,
  Button,
} from "@mui/material";
import axios from "axios";
import React from "react";

function App() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const [message, setMessage] = React.useState("");
  const [errors, setErrors] = React.useState({ email: false, hash: false });
  const onSubmit = (e) => {
    e.preventDefault();
    const { email, hash, wordlist } = e.target.elements;
    let isError = false;
    if (!emailRegex.test(email.value)) {
      isError = true;
      setErrors((prev) => ({ ...prev, email: true }));
    }
    if (hash.value.length > 64) {
      isError = true;
      setErrors((prev) => ({ ...prev, hash: true }));
    }

    if (!isError) {
      const body = {
        email: email.value,
        hash: hash.value,
        wordlist: wordlist.value,
      };
      axios
        .post("http://localhost:8000/break-hash", body, {})
        .then((res) => {
          setMessage("Your hash is being processed by our system. Await an email message with the results!");
        })
        .catch((e) => {
          setMessage("Error occured");
        });
    }
  };

  return (
    <div className="centered h-100">
      <div className="App" style={{ width: 300 }}>
        <div className="field">{message}</div>
        <form onSubmit={onSubmit} className="centered f-column">
          <TextField
            fullWidth
            className="field"
            name="hash"
            label="Hash"
            variant="outlined"
            error={errors.hash}
            helperText={
              errors.hash &&
              "Please insert a hash value no longer than 64 characters"
            }
            onChange={() => setErrors((prev) => ({ ...prev, hash: false }))}
          />
          <TextField
            fullWidth
            className="field"
            name="email"
            label="Email"
            variant="outlined"
            error={errors.email}
            helperText={errors.email && "Please insert a valid email address."}
            onChange={() => setErrors((prev) => ({ ...prev, email: false }))}
          />

          <FormControl className="field" fullWidth>
            <InputLabel variant="standard" htmlFor="uncontrolled-native">
              Wordlist used
            </InputLabel>
            <NativeSelect
              variant="outlined"
              defaultValue='random_words'
              inputProps={{
                name: "wordlist",
              }}
            >
              <option value='english_names'>Popular names in English language</option>
              <option value='random_words'>Random words</option>
              <option value='top_100_passwords'>Top 100 passwords</option>
              <option value='top_1000_family_names'>Top 1000 family names in English language</option>
            </NativeSelect>
          </FormControl>
          <Button type="submit" variant="contained">
            Submit
          </Button>
        </form>
      </div>
    </div>
  );
}

export default App;
