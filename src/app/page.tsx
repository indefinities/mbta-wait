import { getRouteData } from "./lib/data";
import Footer from "./ui/footer";

export default async function Home() {
  const lines = await getRouteData();
  console.log(lines)

  return (
    <div className="">
      <main className="">
        <div>
          
        </div>
      </main>
      <Footer />
    </div>
  );
}
