import ReactQueryProvider from "../components/ReactQueryProvider";
import Home from "../components/Home";

export default function Page() {
  return (
    <ReactQueryProvider>
      <Home />
    </ReactQueryProvider>
  );
}
