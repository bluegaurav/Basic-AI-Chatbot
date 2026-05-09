import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { PREDEFINED_ROLES } from '../types/user';
import { X, Save, User as UserIcon } from 'lucide-react';

interface SettingsProps {
  onClose: () => void;
}

export const Settings = ({ onClose }: SettingsProps) => {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [selectedRole, setSelectedRole] = useState(user?.role?.title || 'General');
  const [context, setContext] = useState(user?.context || '');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.name);
      setSelectedRole(user.role?.title || 'General');
      setContext(user.context || '');
    }
  }, [user]);

  const handleSave = async () => {
    const role = PREDEFINED_ROLES.find((r) => r.title === selectedRole);
    await updateUser({
      name,
      role: role || PREDEFINED_ROLES[5],
      context,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
              <UserIcon className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Settings</h2>
              <p className="text-sm text-gray-500">Customize your AI experience</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Personal Info */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Personal Information
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
                  placeholder="Your name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={user?.email}
                  disabled
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-gray-50 text-gray-500 cursor-not-allowed"
                />
              </div>
            </div>
          </div>

          {/* Role Selection */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Your Role</h3>
            <p className="text-sm text-gray-600 mb-4">
              Select your role to receive tailored responses
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {PREDEFINED_ROLES.map((role) => (
                <button
                  key={role.title}
                  onClick={() => setSelectedRole(role.title)}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    selectedRole === role.title
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-semibold text-gray-900">{role.title}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {role.description}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Context */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Additional Context
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Provide context about your needs for more personalized assistance
            </p>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              rows={4}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none resize-none transition-all"
              placeholder="e.g., I'm working on a React project and need help with state management..."
            />
            <p className="text-xs text-gray-500 mt-2">
              This helps the AI understand your specific needs and provide better responses
            </p>
          </div>

          {/* Save Button */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-200">
            {saved && (
              <span className="text-sm text-green-600 font-medium">
                ✓ Settings saved successfully!
              </span>
            )}
            <div className="ml-auto flex gap-3">
              <button
                onClick={onClose}
                className="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-6 py-2.5 bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-lg font-medium shadow-md hover:shadow-lg transition-all flex items-center gap-2"
              >
                <Save className="w-4 h-4" />
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
