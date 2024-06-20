export default function Header() {
    return (
        <header className="bg-white py-6 px-6 shadow-sm w-full">
            <div className="max-w-7xl mx-auto flex justify-between items-center">
                <h1 className="text-xl text-gray-800 font-semibold">hit</h1>
                <nav>
                    <ul className="flex space-x-4">
                        <li><a href="#home" className="text-gray-600 hover:text-gray-800">Home</a></li>
                        <li><a href="#about" className="text-gray-600 hover:text-gray-800">About</a></li>
                        <li><a href="#services" className="text-gray-600 hover:text-gray-800">Services</a></li>
                        <li><a href="#contact" className="text-gray-600 hover:text-gray-800">Contact</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}