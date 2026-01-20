import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/ui/spinner";
import { Plane, UploadCloud } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { FieldDescription } from "./components/ui/field";

const API_URL = import.meta.env.VITE_API_URL;
const allowedExtensions = ["xlsx"];

function App() {
  const [fileName, setFileName] = useState("Nenhum arquivo selecionado");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const downloadBlob = (blob: Blob, filename: string) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      setFile(null);
      setFileName("Nenhum arquivo selecionado");
      return;
    }

    const extension = selectedFile.name.split(".").pop()?.toLowerCase();

    if (!extension || !allowedExtensions.includes(extension)) {
      toast.error("Formato inválido. Envie um arquivo .xlsx");
      e.target.value = "";
      setFile(null);
      setFileName("Nenhum arquivo selecionado");
      return;
    }

    setFile(selectedFile || null);
    setFileName(selectedFile ? selectedFile.name : "Nenhum arquivo selecionado");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      toast.warning("Selecione um arquivo primeiro.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Erro ao enviar o arquivo");

      const blob = await response.blob();
      downloadBlob(blob, "resultado.zip");
    } catch (err) {
      toast.error("Falha ao processar o arquivo. Verifique o formato e tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-900 flex flex-col">
      <header className="flex items-center gap-3 p-6 border-b border-zinc-700">
        <Plane className="h-10 w-10 text-blue-500" />
        <h1 className="text-4xl font-extrabold text-white tracking-tight">Flight Price</h1>
      </header>

      <main className="flex flex-col flex-grow justify-center items-center px-6">
        <h2 className="text-3xl text-white mb-8 font-semibold">Gere previsões de preço de voos</h2>

        <form
          onSubmit={handleSubmit}
          className="bg-zinc-800 rounded-3xl shadow-xl p-10 w-full max-w-md flex flex-col gap-6"
        >
          <Label htmlFor="fileInput" className="text-gray-300 font-medium">
            {fileName}
          </Label>

          <Field>
            <Input
              id="fileInput"
              type="file"
              accept=".xlsx"
              onChange={handleFileChange}
              className="cursor-pointer text-gray-200"
              disabled={loading}
            />
            <FieldDescription>Selecione um arquivo .xlsx pra enviar</FieldDescription>
          </Field>

          <Button
            type="submit"
            className="w-full flex justify-center items-center gap-2 border-2 border-blue-500 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50"
            disabled={loading || !file}
          >
            <UploadCloud className="h-5 w-5" />
            {loading ? (
              <>
                <Spinner /> Processando...
              </>
            ) : (
              "Gerar previsões"
            )}
          </Button>
        </form>
      </main>
    </div>
  );
}

export default App;
