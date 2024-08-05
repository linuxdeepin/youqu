set -e
ROOT_DIR=$(dirname "$(pwd)")

cd ${ROOT_DIR}
docs_path="$( cd "$( dirname "$0")" && pwd)"
if [[ "${docs_path}" != "${PWD}" ]]; then
    cd "${docs_path}" || exit 1
fi

node_version=v18.16.1
opt_node_dir="node${node_version}"

if ! command -v node &> /dev/null; then
    wget https://cdn.npmmirror.com/binaries/node/${node_version}/node-${node_version}-linux-x64.tar.xz
    tar -xvJf node-${node_version}-linux-x64.tar.xz
    sudo rm -rf /opt/${opt_node_dir}
    sudo mv node-${node_version}-linux-x64 /opt/${opt_node_dir}
    sudo rm -rf /usr/local/bin/npm; sudo ln -s /opt/${opt_node_dir}/bin/npm   /usr/local/bin/npm
    sudo rm -rf /usr/local/bin/node; sudo ln -s /opt/${opt_node_dir}/bin/node   /usr/local/bin/node
elif ! command -v pnpm  &> /dev/null; then
    npm config set registry https://registry.npmmirror.com
    npm install -g pnpm
    sudo rm -rf /usr/local/bin/pnpm; sudo ln -s /opt/${opt_node_dir}/bin/pnpm /usr/local/bin/pnpm
    sudo rm -rf /usr/local/bin/pnpx; sudo ln -s /opt/${opt_node_dir}/bin/pnpx /usr/local/bin/pnpx
fi

pnpm add -D vitepress
pnpm i vitepress-plugin-comment-with-giscus
pnpm i vitepress-plugin-back-to-top
pnpm add -D busuanzi.pure.js
pnpm i medium-zoom
