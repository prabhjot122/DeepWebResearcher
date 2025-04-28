import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Search, NotepadText, FileStack } from 'lucide-react';
import { TbBrandBlogger } from "react-icons/tb";
import { Button } from "./ui/button";

interface EditorSearchBarProps {
  onSearch: (query: string, category: string, additionalInfo: string) => void;
}

const categories = [
  { id: "executive-summary", label: "Executive Summary", icon: <NotepadText size={16} /> },
  { id: "blog-style", label: "Blog Style", icon: <TbBrandBlogger size={16} /> },
  { id: "detailed-report", label: "Detailed Report", icon: <FileStack size={16} /> }
];

export const EditorSearchBar = ({ onSearch }: EditorSearchBarProps) => {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setIsOpen(true);
    }
  };

  const handleModalSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && category) {
      setIsLoading(true);
      try {
        onSearch(query, category, additionalInfo);
        setCategory('');
        setAdditionalInfo('');
        setIsOpen(false);
      } catch (error) {
        console.error('Error starting research:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <div className="editor-search-bar" style={{ 
        display: 'flex', 
        width: '100%',
        margin: '0 10px',
        position: 'relative',
        zIndex: 10
      }}>
        <form onSubmit={handleSubmit} className="w-full relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your query..."
            className="w-full pl-10 pr-4 py-4 rounded-full border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
          />
        </form>
      </div>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Configure your Research</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleModalSubmit} className="space-y-4 p-3">
          <div className="space-y-2">
            <label htmlFor="category" className="text-sm font-medium">
              Category
            </label>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select a category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.id} className="flex items-center gap-2">
                    <span className="mr-2">{cat.icon}</span>
                    {cat.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label htmlFor="additionalInfo" className="text-sm font-medium">
              Additional Information
            </label>
            <textarea
              id="additionalInfo"
              value={additionalInfo}
              onChange={(e) => setAdditionalInfo(e.target.value)}
              className="w-full p-2 border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
              placeholder="Enter any additional information..."
              rows={3}
            />
          </div>
          <Button
            type="submit"
            disabled={isLoading || !category}
            className="w-full"
          >
            {isLoading ? 'Generating...' : 'Generate'}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
};

